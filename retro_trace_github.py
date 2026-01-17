import yfinance as yf
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

# --- 從 GitHub Secrets 讀取設定 ---
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

RECEIVER_EMAIL = GMAIL_USER # 預設寄給自己

def get_analysis():
    tickers = {"大盤": "^TWII", "台積電": "2330.TW"}
    periods = {"半年": 125, "一年": 250, "兩年": 500}

    alert_triggered = False
    report_content = "### 台股回檔監測報告 ###\n\n"
    max_drawdown_level = 0

    for name, symbol in tickers.items():
        data = yf.Ticker(symbol).history(period="3y")
        if data.empty: continue

        current_price = data['Close'].iloc[-1]
        report_content += f"【{name}】目前價格: {current_price:.2f}\n"

        for p_name, days in periods.items():
            high = data['High'].iloc[-days:].max()
            dd = (1 - current_price / high) * 100
            report_content += f"  * {p_name}區間：高點 {high:.2f} / 回檔 {dd:.2f}%\n"

            # 判斷是否觸發門檻 (以一年高點回檔為基準)
            if p_name == "一年":
                if dd >= 5: alert_triggered = True
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

    return alert_triggered, report_content

def send_email(content: str):
    msg = MIMEText(content)
    msg['Subject'] = f"{content.splitlines()[-1]}【台股回檔通知】 - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = GMAIL_USER
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, RECEIVER_EMAIL, msg.as_string())

if __name__ == "__main__":
    triggered, content = get_analysis()
    # 只要有回檔 5% 以上就寄信，或你可以改成每次收盤都寄
    if triggered:
        send_email(content)
        print("已發送回檔警報郵件")
    else:
        print("未達回檔門檻，不發送郵件")
