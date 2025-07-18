from datetime import datetime
import pytz


def is_restaurant_open(restaurant):
    now = datetime.now(pytz.timezone('Asia/Tehran'))
    today = now.weekday()
    current_time = now.time()
    return restaurant.working_hours.filter(
        day_of_week=today,
        open_time__lte=current_time,
        close_time__gte=current_time
    ).exists()
