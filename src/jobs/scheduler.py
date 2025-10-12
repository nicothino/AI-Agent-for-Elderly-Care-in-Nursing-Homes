from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.daily_summary_job import run_daily_summary
from jobs.weekly_report_job import run_weekly_report

def start_jobs():
    scheduler = AsyncIOScheduler(timezone="America/Bogota")

    # Job diario: resumen emocional a las 21:00
    scheduler.add_job(run_daily_summary, "cron", hour=21, minute=0)

    # Job semanal: reporte emocional los domingos 22:00
    scheduler.add_job(run_weekly_report, "cron", day_of_week="sun", hour=22, minute=0)

    scheduler.start()
    print("🕒 Jobs programados: resumen diario y reporte semanal.")
