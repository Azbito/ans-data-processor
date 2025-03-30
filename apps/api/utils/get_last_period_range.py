from datetime import datetime, timedelta

def get_last_period_range(period: str, date: datetime = datetime.now()) -> tuple:
    if period == 'quarterly':
        quarter = (date.month - 1) // 3
        if quarter == 0:
            year = date.year - 1
            start_month = 10
        else:
            year = date.year
            start_month = (quarter - 1) * 3 + 1

        start_date = datetime(year, start_month, 1)

        end_month = start_month + 2
        if end_month > 12:
            end_month -= 12
            year += 1
        
        if end_month > 12:
            end_month = 1
            year += 1
        
        end_date = datetime(year, end_month, 1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)

    elif period == 'yearly':
        start_date = datetime(date.year, 1, 1)
        end_date = datetime(date.year, 12, 31, 23, 59, 59, 999999)

    return start_date, end_date
