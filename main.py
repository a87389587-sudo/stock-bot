import pandas as pd
import requests
import os
from datetime import datetime

# 從 GitHub Secrets 讀取您剛才設定的鑰匙
LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
LINE_USER_ID = os.environ.get('LINE_USER_ID')

def get_chip_data(stock_id):
    """獲取三大法人買賣超數據 (範例使用 mock 數據，實務上可串接 API)"""
    # 這裡可以串接證交所或財報狗等 API
    # 為了測試，我們先產生一份簡單的報告內容
    today = datetime.now().strftime('%Y-%m-%d')
    report = f"\n📈 【{stock_id} 籌碼快訊】 {today}\n"
    report += "-------------------\n"
    report += "外資：買超 +1,250 張\n"
    report += "投信：買超 +300 張\n"
    report += "自營商：賣超 -150 張\n"
    report += "結論：法人連三買，短線偏多看待。\n"
    return report

def send_line_message(message):
    """透過 LINE Messaging API 發送訊息"""
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    data = {
        'to': LINE_USER_ID,
        'messages': [{'type': 'text', 'text': message}]
    }
    res = requests.post(url, headers=headers, json=data)
    return res.status_code

def main():
    # 您感興趣的核心持股
    target_stocks = ['2330', '2454']
    full_report = "📊 陳先生，今日法人籌碼動態如下："
    
    for stock in target_stocks:
        full_report += get_chip_data(stock)
    
    status = send_line_message(full_report)
    if status == 200:
        print("報告發送成功！")
    else:
        print(f"發送失敗，錯誤代碼：{status}")

if __name__ == "__main__":
    main()
