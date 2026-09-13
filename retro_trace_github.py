import yfinance as yf
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

# --- 從 GitHub Secrets / 環境變數讀取設定 ---
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
TRIGGER_EVENT = os.getenv('TRIGGER_EVENT', 'unknown')

# 主收件人固定為寄件者自己；第二收件人則由 Secret 帶入，可為單一信箱或逗號分隔多個信箱
RECEIVER_EMAIL = GMAIL_USER
SECOND_RECEIVER = os.getenv('SECOND_RECEIVER', '')


def build_recipients(trigger_event, trigger_state, receiver_email, second_receiver):
    """依照觸發來源與回檔區間門檻決定寄送清單。"""
    if trigger_event == 'workflow_dispatch':
        return [receiver_email] if receiver_email else []

    # 第二收件人可為單一信箱或逗號分隔多個信箱
    second_list = [x.strip() for x in second_receiver.split(',') if x.strip()] if second_receiver else []

    # 單月 5% / 半年 8% / 一年 8%：寄給所有人（主收件人 + 第二收件人）
    if trigger_state.get('單月') or trigger_state.get('半年') or trigger_state.get('一年_8'):
        recipients = []
        if receiver_email:
            recipients.append(receiver_email)
        recipients.extend(second_list)

        seen = set()
        unique = []
        for recipient in recipients:
            if recipient not in seen:
                seen.add(recipient)
                unique.append(recipient)
        return unique

    # 一年 5%：僅寄給主收件人
    if trigger_state.get('一年_5') and receiver_email:
        return [receiver_email]

    return []


def get_analysis():
    tickers = {"大盤": "^TWII", "台積電": "2330.TW"}
    periods = {"單月": 30, "半年": 125, "一年": 250, "兩年": 500}

    report_content = "### 台股回檔監測報告 ###\n\n"
    max_drawdown_level = 0
    trigger_state = {"單月": False, "半年": False, "一年_5": False, "一年_8": False}

    for name, symbol in tickers.items():
        data = yf.Ticker(symbol).history(period="3y")
        if data.empty:
            continue

        current_price = yf.Ticker(symbol).fast_info['last_price']
        report_content += f"【{name}】目前價格: {current_price:.2f}\n"

        for p_name, days in periods.items():
            high = data['High'].iloc[-days:].max()
            dd = (1 - current_price / high) * 100
            report_content += f"  * {p_name}區間：高點 {high:.2f} / 回檔 {dd:.2f}%\n"

            # 兩年區間只顯示在內容，不納入觸發條件
            if p_name == "兩年":
                continue

            # 單月 5% => 全部收件人
            if p_name == "單月" and dd >= 5:
                trigger_state["單月"] = True

            # 半年 8% => 全部收件人
            elif p_name == "半年" and dd >= 8:
                trigger_state["半年"] = True

            # 一年 5% => 主收件人；一年 8% => 全部收件人
            elif p_name == "一年" and dd >= 5:
                if dd >= 8:
                    trigger_state["一年_8"] = True
                else:
                    trigger_state["一年_5"] = True

            # 兩年區間不納入 max_drawdown 的警示總評
            max_drawdown_level = max(max_drawdown_level, dd)

        report_content += "\n"

    # 增加行動建議
    report_content += "--- 總結 ---\n"
    if max_drawdown_level >= 15:
        report_content += "🔥 警報：市場進入超跌區"
    elif max_drawdown_level >= 10:
        report_content += "💎 提醒：中度修正達成"
    elif max_drawdown_level >= 5:
        report_content += "📈 提示：短期整理"
    else:
        report_content += "✅ 市場趨勢強勁。"

    return trigger_state, max_drawdown_level, report_content


def send_email(content: str, recipients: list):
    if not recipients:
        print("未達寄送門檻，不發送郵件")
        return

    subject = f"{content.splitlines()[-1]}【台股回檔通知】 - {datetime.now().strftime('%Y-%m-%d')}"

    # 一封信內容，搭配一個收件人清單，避免每位收件人都拆成個別信件
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, recipients, msg.as_string())


if __name__ == "__main__":
    trigger_state, max_drawdown_level, content = get_analysis()
    print(content)

    recipients = build_recipients(TRIGGER_EVENT, trigger_state, RECEIVER_EMAIL, SECOND_RECEIVER)
    if recipients:
        send_email(content, recipients)
        print("已發送回檔警報郵件")
    else:
        print("未達回檔門檻，不發送郵件")
