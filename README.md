# Taiwan Stock Retrace Monitor - 台股回檔監控系統

[中文說明](#chinese) | [English Description](#english)

---

<a name="chinese"></a>

# 🇹🇼 台股回檔監控系統

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Github Actions](https://img.shields.io/badge/Actions-Scheduled-success.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 專案簡介
這是一個自動化的台股監控工具，旨在追蹤標的（如台股基金、ETF 或個別股票）相對於 **年度最高點** 的回檔幅度。透過 GitHub Actions 每日自動執行，當標的跌幅達到預設的「回檔買進區間」時，系統將自動發送 Email 提醒，協助投資者克服恐懼，落實紀律投資。

## ✨ 主要功能
* **多標的支援**：支援所有 Yahoo Finance 可查詢之台股代號（如 `2330.TW`, `0050.TW`）。
* **動態回檔計算**：自動抓取過去 252 個交易日數據，計算滾動最高點（Rolling High）與當前跌幅。
* **雲端全自動化**：不需維持電腦開啟，利用 GitHub Actions 於每日台股收盤後（13:30 CST）自動掃描。
* **隱私安全**：採用 GitHub Secrets 加密技術，確保 Gmail 授權金鑰不外洩。

## 🛠️ 技術說明
* **數據來源**：`yfinance` (Yahoo Finance API)
* **資料處理**：`pandas`, `numpy`
* **自動化排程**：GitHub Actions (Ubuntu-latest)
* **郵件通知**：Python `smtplib`
* **核心邏輯**：實作了基於一年（252 交易日）最高價的跌幅公式。
* **環境變數架構**：定義了 `GMAIL_USER` 與 `GMAIL_PASSWORD` 接口。

---

## 🚀 快速開始

### 1. 取得 Gmail 應用程式密碼
請至 Google 帳號安全性設定中開啟「兩步驗證」，並產生一組 16 位元的 **「應用程式密碼 (App Password)」**。

### 2. 設定 GitHub Secrets
前往 `Settings > Secrets and variables > Actions`，新增：
* `GMAIL_USER`: 您的 Gmail 帳號。
* `GMAIL_PASSWORD`: 16 位應用程式密碼。

### 3. 自定義監控標的
編輯 `retro_trace_github.py` 中的 `ticker_symbol` 變數。

## 📅 執行時間說明
本系統設定為週一至週五 **台灣時間 13:30 (UTC 05:30)** 執行。

> [!IMPORTANT]
> **關於執行延遲**：由於 GitHub Actions 的免費伺服器排隊機制，自動排程通常會有 **10 到 30 分鐘的隨機延遲**。若任務未準時於 13:30 啟動，屬正常現象。

## 📝 免責聲明
本工具僅供策略研究使用，不保證數據之絕對準確性。投資者應自行評估風險。

---

<a name="english"></a>

# 🇹🇼 Taiwan Stock Retrace Monitor

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Github Actions](https://img.shields.io/badge/Actions-Scheduled-success.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Project Introduction
An automated monitoring tool for the Taiwan stock market, tracking drawdowns relative to **annual highs**. Using GitHub Actions, the system sends email alerts when prices fall into a predefined "buy zone," assisting disciplined investing.

## ✨ Key Features
* **Multi-Target Support**: Supports any ticker on Yahoo Finance (e.g., `2330.TW`, `0050.TW`).
* **Dynamic Drawdown Calculation**: Computes rolling highs and drawdowns from the past 252 trading days.
* **Cloud Automation**: Runs automatically via GitHub Actions post-market (13:30 CST).
* **Privacy & Security**: Secured with GitHub Secrets for Gmail authorization.

## 🛠️ Technical Specifications
* **Data Source**: `yfinance` (Yahoo Finance API)
* **Data Processing**: `pandas`, `numpy`
* **Automation**: GitHub Actions (Ubuntu-latest)
* **Core Logic**: Drawdown formula based on 1-year (252 trading days) rolling high.
* **Environment Variables**: Defined `GMAIL_USER` and `GMAIL_PASSWORD` interfaces.

---

## 🚀 Quick Start

### 1. Obtain Gmail App Password
Enable "2-Step Verification" in your Google Account and generate a 16-digit **"App Password."**

### 2. Configure GitHub Secrets
Go to `Settings > Secrets and variables > Actions`, and add:
* `GMAIL_USER`: Your Gmail account.
* `GMAIL_PASSWORD`: The 16-digit App Password.

### 3. Customize Targets
Edit the `ticker_symbol` variable in `retro_trace_github.py`.

## 📅 Execution Schedule
The system is scheduled for Monday through Friday at **13:30 Taiwan Time (05:30 UTC)**.

> [!IMPORTANT]
> **Scheduling Delay**: Due to GitHub Actions' shared infrastructure, scheduled tasks may experience a **10 to 30-minute delay** depending on server load. It is normal if the workflow does not start precisely at 13:30.

## 📝 Disclaimer
This tool is for strategic research only. Data accuracy is not guaranteed. Investors should assess risks independently.