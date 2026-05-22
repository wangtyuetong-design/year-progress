import datetime
import json
import os
import math
import urllib.request

QUOTES = [
    "不要等准备好了才开始，开始了才会准备好。",
    "每一个今天，都是余生最年轻的一天。",
    "方向对了，不怕慢。",
    "你现在的努力，是在给未来的自己铺路。",
    "比昨天好一点点，就是成长。",
    "做完比做好更重要，先完成，再完善。",
    "进入未知领域，修正航向，反复迭代。",
    "时间不等人，但时间也不亏人。",
    "你以为的绕路，往往是最短的路。",
    "今天种下的种子，会在你看不见的地方生长。",
]

def make_bar(pct, width=20):
    filled = math.floor(pct / 100 * width)
    return "▓" * filled + "░" * (width - filled)

def load_goals():
    try:
        with open("goals.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def main():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    year = now.year
    start = datetime.datetime(year, 1, 1, tzinfo=now.tzinfo)
    end = datetime.datetime(year + 1, 1, 1, tzinfo=now.tzinfo)

    today_pct = int((now - start) / (end - start) * 100)
    days_left = (end - now).days

    is_manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

    if not is_manual:
        yesterday = now - datetime.timedelta(days=1)
        yesterday_pct = int((yesterday - start) / (end - start) * 100)
        if today_pct == yesterday_pct:
            print(f"today is still {today_pct}%, skip")
            return

    bar = make_bar(today_pct)
    quote = QUOTES[today_pct % len(QUOTES)]

    goals = load_goals()
    goal_lines = ""
    if goals:
        goal_lines = "\n\n📋 年度目标进展："
        for g in goals:
            done = g.get("done", 0)
            target = g.get("target", 1)
            name = g.get("name", "")
            g_pct = int(done / target * 100)
            g_bar = make_bar(g_pct, width=10)
            goal_lines += f"\n{name}：{done}/{target}  {g_bar} {g_pct}%"

    prefix = "🚀 通道测试！" if is_manual else "⏳"
    text = f"""{prefix} {year}年进度播报

{bar} {today_pct}%
📅 已过 {today_pct} 格，还剩 {days_left} 天{goal_lines}

💬 {quote}"""

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