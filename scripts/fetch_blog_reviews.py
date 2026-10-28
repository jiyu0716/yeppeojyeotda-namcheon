"""네이버 검색 API로 '예뻐졌다 남천점' 블로그 후기를 받아 blog-reviews.json에 저장한다.

GitHub Actions가 하루 한 번 실행한다 (.github/workflows/blog-reviews.yml).
키는 코드에 적지 않고 저장소 Secrets(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET)에서 받는다.
"""
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

QUERY = "예뻐졌다 남천점"
# 다른 지점·다른 가게 글이 섞이지 않게, 제목이나 요약에 두 단어가 모두 있는 글만 남긴다
MUST_INCLUDE = ("예뻐졌다", "남천")
MAX_ITEMS = 9
OUT = os.path.join(os.path.dirname(__file__), "..", "blog-reviews.json")


def clean(text):
    # API는 검색어를 <b>로 감싸서 준다 → 태그를 지우고 &amp; 같은 문자를 되돌린다
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def fetch(client_id, client_secret):
    url = "https://openapi.naver.com/v1/search/blog.json?" + urllib.parse.urlencode(
        {"query": QUERY, "display": 50, "sort": "date"})
    req = urllib.request.Request(url, headers={
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    })
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)


def pick(data):
    items = []
    for raw in data.get("items", []):
        title, summary = clean(raw.get("title")), clean(raw.get("description"))
        link = raw.get("link", "")
        if not link.startswith("https://"):
            continue
        if not all(word in title + " " + summary for word in MUST_INCLUDE):
            continue
        date = raw.get("postdate", "")
        items.append({
            "title": title,
            "summary": summary,
            "blogger": clean(raw.get("bloggername")),
            "date": f"{date[:4]}-{date[4:6]}-{date[6:8]}" if len(date) == 8 else "",
            "link": link,
        })
        if len(items) == MAX_ITEMS:
            break
    return items


def main():
    client_id = os.environ.get("NAVER_CLIENT_ID", "").strip()
    client_secret = os.environ.get("NAVER_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        sys.exit("NAVER_CLIENT_ID / NAVER_CLIENT_SECRET이 없습니다. 저장소 Settings → Secrets and variables → Actions에 등록해 주세요.")

    items = pick(fetch(client_id, client_secret))

    try:
        old = json.load(open(OUT, encoding="utf-8"))
    except (OSError, ValueError):
        old = {}
    # 글 목록이 그대로면 파일을 건드리지 않는다 → 매일 쓸데없는 커밋이 생기지 않는다
    if old.get("items") == items:
        print(f"변경 없음 ({len(items)}개)")
        return

    kst = datetime.now(timezone(timedelta(hours=9)))
    data = {"query": QUERY, "updated": kst.strftime("%Y-%m-%d"), "items": items}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"저장 완료: {len(items)}개")


if __name__ == "__main__":
    main()
