"""Naver Shopping search for the researcher: top products and price distribution.

Usage:
  python3 scripts/naver_shopping.py "이끼 화분" --display 40

Needs NAVER_CLIENT_ID / NAVER_CLIENT_SECRET (free, developers.naver.com → 검색 API).
Without them it prints {"skipped": ...} and exits 0 so the researcher falls back to WebSearch.
"""
import argparse
import json
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

from _env import load_env


def search(query: str, display: int, client_id: str, secret: str) -> list[dict]:
    url = "https://openapi.naver.com/v1/search/shop.json?" + urllib.parse.urlencode(
        {"query": query, "display": display, "sort": "sim"}
    )
    req = urllib.request.Request(url, headers={
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": secret,
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["items"]


def summarize(query: str, items: list[dict]) -> dict:
    prices = sorted(int(i["lprice"]) for i in items if i.get("lprice", "").isdigit() and int(i["lprice"]) > 0)
    top = [
        {
            "title": re.sub(r"<[^>]+>", "", i["title"]),
            "price": int(i["lprice"]) if i.get("lprice", "").isdigit() else None,
            "mall": i.get("mallName"),
            "category": " > ".join(c for c in (i.get("category1"), i.get("category2"), i.get("category3")) if c),
            "link": i.get("link"),
        }
        for i in items[:10]
    ]
    stats = None
    if prices:
        stats = {
            "n": len(prices),
            "min": prices[0],
            "median": int(statistics.median(prices)),
            "max": prices[-1],
        }
    return {"query": query, "price_stats": stats, "top10": top}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--display", type=int, default=40)
    args = parser.parse_args()

    load_env()
    client_id = os.environ.get("NAVER_CLIENT_ID")
    secret = os.environ.get("NAVER_CLIENT_SECRET")
    if not (client_id and secret):
        print(json.dumps({"skipped": "NAVER_CLIENT_ID / NAVER_CLIENT_SECRET not set", "query": args.query},
                         ensure_ascii=False))
        return 0

    try:
        items = search(args.query, max(1, min(args.display, 100)), client_id, secret)
    except urllib.error.HTTPError as e:
        print(f"Naver API error {e.code}: {e.read().decode(errors='replace')[:300]}", file=sys.stderr)
        return 1

    print(json.dumps(summarize(args.query, items), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
