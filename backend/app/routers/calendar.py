from fastapi import APIRouter
from datetime import datetime, date
from typing import Optional
from ..schemas import CalendarMonthRequest, CalendarMonthResponse, CalendarDayInfo

router = APIRouter(prefix="/calendar", tags=["calendar"])

TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
LUNAR_MONTHS = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']
LUNAR_DAYS = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
              '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
              '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
WEEKDAYS_CN = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
WEEKDAYS_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTH_NAMES = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']

SOLAR_TERMS = [
    (2, 4, '立春'), (2, 19, '雨水'),
    (3, 6, '惊蛰'), (3, 21, '春分'),
    (4, 5, '清明'), (4, 20, '谷雨'),
    (5, 6, '立夏'), (5, 21, '小满'),
    (6, 6, '芒种'), (6, 21, '夏至'),
    (7, 7, '小暑'), (7, 23, '大暑'),
    (8, 8, '立秋'), (8, 23, '处暑'),
    (9, 8, '白露'), (9, 23, '秋分'),
    (10, 8, '寒露'), (10, 23, '霜降'),
    (11, 8, '立冬'), (11, 23, '小雪'),
    (12, 7, '大雪'), (12, 22, '冬至'),
    (1, 6, '小寒'), (1, 20, '大寒')
]

HOLIDAYS = {
    (1, 1): '元旦',
    (2, 14): '情人节',
    (3, 8): '妇女节',
    (3, 12): '植树节',
    (4, 1): '愚人节',
    (5, 1): '劳动节',
    (5, 4): '青年节',
    (6, 1): '儿童节',
    (7, 1): '建党节',
    (8, 1): '建军节',
    (9, 10): '教师节',
    (10, 1): '国庆节',
    (12, 25): '圣诞节'
}


def get_lunar_info(dt: date):
    from datetime import date as dt_date
    base_date = dt_date(1900, 1, 31)
    delta = (dt - base_date).days
    
    lunar_year = 1900
    lunar_month = 1
    lunar_day = 1
    
    lunar_days = [29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30]
    
    day_of_year = delta
    year_days = sum(lunar_days)
    
    while day_of_year >= year_days:
        day_of_year -= year_days
        lunar_year += 1
        if (lunar_year % 4 == 0 and lunar_year % 100 != 0) or (lunar_year % 400 == 0):
            year_days = 355
        else:
            year_days = 354
    
    month_idx = 0
    while day_of_year >= lunar_days[month_idx]:
        day_of_year -= lunar_days[month_idx]
        month_idx += 1
        if month_idx >= 12:
            month_idx = 0
    
    lunar_month = month_idx + 1
    lunar_day = day_of_year + 1
    
    gan_index = (lunar_year - 4) % 10
    zhi_index = (lunar_year - 4) % 12
    lunar_year_str = f"{TIAN_GAN[gan_index]}{DI_ZHI[zhi_index]}年"
    
    return lunar_year_str, LUNAR_MONTHS[lunar_month - 1], LUNAR_DAYS[lunar_day - 1]


def get_solar_term(dt: date) -> Optional[str]:
    for month, day, name in SOLAR_TERMS:
        if dt.month == month and dt.day == day:
            return name
    return None


def get_holiday(dt: date) -> Optional[str]:
    return HOLIDAYS.get((dt.month, dt.day))


def get_days_in_month(year: int, month: int) -> int:
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - date(year, month, 1)).days


def get_first_day_weekday(year: int, month: int) -> int:
    first_day = date(year, month, 1)
    return first_day.weekday()


@router.post("/month", response_model=CalendarMonthResponse)
def get_calendar_month(request: CalendarMonthRequest):
    now = datetime.now()
    year = request.year if request.year else now.year
    month = request.month if request.month else now.month
    
    today = now.date()
    days_in_month = get_days_in_month(year, month)
    first_day_weekday = get_first_day_weekday(year, month)
    
    days = []
    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        weekday_idx = current_date.weekday()
        
        lunar_year, lunar_month, lunar_day = get_lunar_info(current_date)
        solar_term = get_solar_term(current_date)
        holiday = get_holiday(current_date)
        
        day_info = CalendarDayInfo(
            year=year,
            month=month,
            day=day,
            weekday=WEEKDAYS_CN[weekday_idx],
            weekday_en=WEEKDAYS_EN[weekday_idx],
            lunar_year=lunar_year,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            solar_term=solar_term,
            is_holiday=holiday is not None,
            holiday_name=holiday,
            is_today=current_date == today
        )
        days.append(day_info)
    
    return CalendarMonthResponse(
        year=year,
        month=month,
        month_name=MONTH_NAMES[month - 1],
        days=days,
        first_day_weekday=first_day_weekday,
        total_days=days_in_month
    )


@router.get("/today")
def get_today_info():
    now = datetime.now()
    today = now.date()
    weekday_idx = today.weekday()
    
    lunar_year, lunar_month, lunar_day = get_lunar_info(today)
    solar_term = get_solar_term(today)
    holiday = get_holiday(today)
    
    return {
        "year": today.year,
        "month": today.month,
        "day": today.day,
        "weekday": WEEKDAYS_CN[weekday_idx],
        "weekday_en": WEEKDAYS_EN[weekday_idx],
        "lunar_year": lunar_year,
        "lunar_month": lunar_month,
        "lunar_day": lunar_day,
        "solar_term": solar_term,
        "is_holiday": holiday is not None,
        "holiday_name": holiday,
        "datetime_str": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(now.timestamp())
    }
