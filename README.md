# reddit-approved-poster

A small personal script that lets me, Wade Mohlmann, post and comment on Reddit from my own account, u/KingWadelz, only after I have read and approved the exact text and target.

## Purpose

This is a personal, non-commercial student project. It supports my Graduation Realisation project at Breda University of Applied Sciences (BUas), which is about task-initiation support for students with ADHD. I use it to take part in peer-support conversations and, where allowed, to share research-recruitment posts.

It supports outreach for my BUas graduation project on task-initiation support for students with ADHD (the Nudge prototype and the INQUIRER interview study). Those project repos are private for now.

## How it works

- It acts only as my own account, u/KingWadelz, via OAuth (a Reddit "script" app with a refresh token). No password is stored.
- Every write needs my explicit approval. The script prints the exact text and target, and nothing is sent unless I type `APPROVE`.
- It is human-in-the-loop. Nothing is scheduled and nothing auto-publishes.
- It is a dry run by default. It only submits to Reddit when `--live` is passed and I have typed `APPROVE`.
- Each submitted item is recorded in a local `audit.log` (timestamp, target, permalink).
- One draft, one submission per run. There are no loops, schedules, or bulk features.

## Volume and where it is used

- Low volume: about 1-3 peer-support comments per week.
- Occasional research-recruitment posts, only where subreddit rules and moderators allow it. Currently that is r/UniUK (per its wiki) and r/SampleSize.
- I follow each subreddit's rules. In r/adhd_college and r/ADHD I only take part in peer support, with no recruitment posts.

## What it will NOT do

- Use multiple accounts
- Karma farming
- Voting
- Spam, or cross-posting identical text
- Mass DMs
- Scraping
- ML or AI training on Reddit data
- Inferring sensitive traits about anyone
- Data resale

## Compliance

This project complies with Reddit's Responsible Builder Policy and the Reddit Data API Terms.

## Status

Awaiting Reddit Data API approval.

## Usage

```
pip install -r requirements.txt

export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
export REDDIT_REFRESH_TOKEN=...
# optional, this is the default:
export REDDIT_USER_AGENT="script:reddit-approved-poster:v0.1 (by u/KingWadelz)"

python poster.py example-draft.md          # dry run (default), nothing is sent
python poster.py example-draft.md --live   # shows the draft, then asks me to type APPROVE
```

See `example-draft.md` for the draft format.

## Contact

Wade Mohlmann, wade24609@gmail.com

## License

MIT, see `LICENSE`.
