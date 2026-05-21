import datetime
import json
import os
import urllib.request

def main():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    year = now.year
    start = datetime.datetime(year, 1, 1, tzinfo=now.tzinfo)
    end = datetime.datetime(year + 1, 1, 1, tzinfo=now.tzinfo)

    today_pct = int((now - start) / (end - start) * 100)

    is_manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

    if not is_manual:
        yesterday = now - datetime.timedelta(days=1)
        yesterday_pct = int((yesterday - start) / (end - start) * 100)
        if today_pct == yesterday_pct:
            print(f"today is still {today_pct}%, skip")
            return

    icon = "🚀 通道测试成功！" if is_manual else "⏳"
    text = f"{icon} {year} 年已完成 {today_pct}%"

    webhook = os.environ.get("FEISHU_WEBHOOK")
    if not webhook:
        print("FEISHU_WEBHOOK not set")
        return

    body = json.dumps({"msg_type": "text", "content": {"text": text}}).encode()
    req = urllib.request.Request(webhook, data=body, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)
    print(f"sent: {text}")

if __name__ == "__main__":
    main()
