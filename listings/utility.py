from datetime import datetime
import pytz

def get_naive_cutoff_time():
    now = datetime.utcnow()
    cutoff_time = datetime(now.year, now.month, now.day, 3, 30, 0, 0, tzinfo=pytz.utc)
    naive_cutoff_time = cutoff_time.replace(tzinfo=None)
    return now, naive_cutoff_time
