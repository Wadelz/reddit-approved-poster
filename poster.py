#!/usr/bin/env python3
"""reddit-approved-poster: submit ONE human-approved post or comment as u/KingWadelz.

Dry run by default. Pass --live to actually submit, and even then nothing is sent
unless you type APPROVE after reviewing the exact text and target.

Credentials come from environment variables (never from this file):
  REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REFRESH_TOKEN
  REDDIT_USER_AGENT (optional)
"""

import argparse
import os
import sys
from datetime import datetime, timezone

DEFAULT_USER_AGENT = "script:reddit-approved-poster:v0.1 (by u/KingWadelz)"
EXPECTED_ACCOUNT = "KingWadelz"
AUDIT_LOG = "audit.log"


def parse_draft(path):
    """Read a draft: 'key: value' header lines, a line with only ---, then the body."""
    with open(path, encoding="utf-8") as f:
        text = f.read().replace("\r\n", "\n")

    header, sep, body = text.partition("\n---\n")
    if not sep:
        sys.exit("Draft needs a header, then a line with only ---, then the body.")

    meta = {}
    for line in header.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, colon, value = line.partition(":")
        if not colon:
            sys.exit(f"Bad header line: {line!r}")
        meta[key.strip().lower()] = value.strip()

    body = body.strip()
    if not body:
        sys.exit("Draft body is empty.")

    has_subreddit = bool(meta.get("subreddit"))
    has_parent = bool(meta.get("parent"))
    if has_subreddit == has_parent:
        sys.exit("Header needs exactly one of 'subreddit' (new post) or 'parent' (comment reply).")

    if has_subreddit:
        name = meta["subreddit"]
        meta["subreddit"] = name[2:] if name.lower().startswith("r/") else name
        if not meta.get("title"):
            sys.exit("A new post needs a 'title'.")
    elif not meta["parent"].startswith(("t3_", "t1_")):
        sys.exit("'parent' must be a t3_ (post) or t1_ (comment) id.")

    return meta, body


def describe_target(meta):
    if meta.get("subreddit"):
        return f"r/{meta['subreddit']} (new text post)"
    return f"reply to {meta['parent']}"


def connect():
    import praw  # imported here so dry runs work without credentials

    missing = [v for v in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_REFRESH_TOKEN")
               if not os.environ.get(v)]
    if missing:
        sys.exit("Missing environment variables: " + ", ".join(missing))

    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        refresh_token=os.environ["REDDIT_REFRESH_TOKEN"],
        user_agent=os.environ.get("REDDIT_USER_AGENT", DEFAULT_USER_AGENT),
    )
    me = reddit.user.me()
    if me is None or me.name.lower() != EXPECTED_ACCOUNT.lower():
        sys.exit(f"Refusing to post: authenticated account is not u/{EXPECTED_ACCOUNT}.")
    return reddit


def submit(reddit, meta, body):
    if meta.get("subreddit"):
        thing = reddit.subreddit(meta["subreddit"]).submit(
            title=meta["title"], selftext=body, flair_id=meta.get("flair_id") or None
        )
    elif meta["parent"].startswith("t3_"):
        thing = reddit.submission(id=meta["parent"][3:]).reply(body)
    else:
        thing = reddit.comment(id=meta["parent"][3:]).reply(body)
    return "https://www.reddit.com" + thing.permalink


def append_audit(target, permalink):
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{stamp}\t{target}\t{permalink}\n")


def main():
    parser = argparse.ArgumentParser(description="Submit one human-approved Reddit post or comment.")
    parser.add_argument("draft", help="path to a draft file (see example-draft.md)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="show the draft and exit (default)")
    mode.add_argument("--live", action="store_true", help="submit after you type APPROVE")
    args = parser.parse_args()

    meta, body = parse_draft(args.draft)
    target = describe_target(meta)

    print("=" * 60)
    print(f"Account: u/{EXPECTED_ACCOUNT}")
    print(f"Target:  {target}")
    if meta.get("title"):
        print(f"Title:   {meta['title']}")
    print("-" * 60)
    print(body)
    print("=" * 60)

    if not args.live:
        print("Dry run: nothing was sent. Re-run with --live to submit.")
        return

    answer = input("Type APPROVE to submit exactly this text to this target: ")
    if answer.strip() != "APPROVE":
        print("Not approved. Nothing was sent.")
        return

    reddit = connect()
    permalink = submit(reddit, meta, body)
    append_audit(target, permalink)
    print(f"Submitted: {permalink}")


if __name__ == "__main__":
    main()
