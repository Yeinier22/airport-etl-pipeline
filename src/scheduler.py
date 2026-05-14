import os
import time

import schedule

try:
    from logger import setup_logger
    from main import run_pipeline
except ImportError:
    from src.logger import setup_logger
    from src.main import run_pipeline


logger = setup_logger()


def _get_interval_hours():
    value = os.getenv("SCHEDULE_EVERY_HOURS", "24")
    try:
        interval = int(value)
    except ValueError as exc:
        raise ValueError("SCHEDULE_EVERY_HOURS must be an integer") from exc

    if interval <= 0:
        raise ValueError("SCHEDULE_EVERY_HOURS must be greater than 0")

    return interval


def _should_run_on_start():
    return os.getenv("RUN_ON_START", "true").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
    }


def scheduled_job():
    logger.info("Scheduled pipeline run started")
    try:
        run_pipeline()
        logger.info("Scheduled pipeline run finished")
    except Exception as exc:
        logger.error(f"Scheduled pipeline run failed: {exc}")


def start_scheduler(run_once=False):
    interval_hours = _get_interval_hours()
    schedule.clear()
    schedule.every(interval_hours).hours.do(scheduled_job)

    logger.info(f"Scheduler started with interval {interval_hours} hour(s)")
    print(f"Scheduler running every {interval_hours} hour(s)")

    if run_once or _should_run_on_start():
        scheduled_job()

    if run_once:
        return

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    start_scheduler()