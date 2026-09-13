# Alltech scheduler

Three jobs, run by the server's cron. Each run starts a container, does one
thing, and exits. Nothing runs in between.

```
send_sales_report      emails the sales report for completed, unreported sales
send_daily_insights    yesterday's AI insight, pushed to managers
send_weekly_insights   this week's AI insight, pushed to managers
```

## Why there is no Celery here any more

There was Celery, a beat schedule, a broker and a worker held open all day —
for three jobs. The server's cron is the scheduler now, so Beat would be a
second scheduler disagreeing with it, and the broker existed only to carry
messages between two processes that no longer both exist.

`manage.py send_daily_insights` is the whole of what was needed.

## Where it runs

On the **backend** server, not the frontend one. These jobs call the Alltech
API, and from that host they can reach it over the Docker network
(`http://web:8000`) instead of going out through Cloudflare and back in.
`CELERY_KEY` also has to match the backend's, and keeping both in one `.env`
on one machine means there is only one place for it to drift.

## Running one by hand

```bash
docker run --rm --network alltech_default \
  --env-file /opt/alltech/backend/scheduler.env \
  gachar4/alltech-scheduler:alltechv2 send_daily_insights
```

A failed job exits non-zero, so cron reports it instead of the failure
disappearing into a log nobody reads.

## Schedule

See `deploy/crontab.example`. Times are the server's local time — check it is
Africa/Nairobi with `timedatectl`, or every job runs three hours early.
