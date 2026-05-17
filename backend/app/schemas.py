from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class ToolCreate(ToolBase):
    pass


class Tool(ToolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str
    phone: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    username: Optional[str] = None


class TimestampConvertRequest(BaseModel):
    timestamp: Optional[int] = None
    datetime_str: Optional[str] = None
    format: Optional[str] = "%Y-%m-%d %H:%M:%S"


class TimestampConvertResponse(BaseModel):
    timestamp: int
    datetime_str: str
    format: str


class JsonFormatRequest(BaseModel):
    json_str: str
    indent: Optional[int] = 2


class JsonFormatResponse(BaseModel):
    valid: bool
    formatted: Optional[str] = None
    error: Optional[str] = None
    minified: Optional[str] = None


class Md5EncryptRequest(BaseModel):
    text: str
    uppercase: Optional[bool] = False


class Md5EncryptResponse(BaseModel):
    original_text: str
    md5_hash: str
    uppercase: bool


class Md5CompareRequest(BaseModel):
    text: str
    md5_hash: str


class Md5CompareResponse(BaseModel):
    match: bool
    original_text: str
    provided_hash: str


class NumberToChineseRequest(BaseModel):
    number: float


class NumberToChineseResponse(BaseModel):
    number: float
    chinese: str


class RsaKeyGenerateRequest(BaseModel):
    key_size: Optional[int] = 2048


class RsaKeyGenerateResponse(BaseModel):
    public_key: str
    private_key: str
    key_size: int


class RsaEncryptRequest(BaseModel):
    plaintext: str
    public_key: str


class RsaEncryptResponse(BaseModel):
    ciphertext: str
    plaintext: str


class RsaDecryptRequest(BaseModel):
    ciphertext: str
    private_key: str


class RsaDecryptResponse(BaseModel):
    plaintext: str
    ciphertext: str


class TimerCreateRequest(BaseModel):
    name: str
    duration: int


class TimerCreateResponse(BaseModel):
    id: str
    name: str
    duration: int
    created_at: str


class TimerStatusResponse(BaseModel):
    id: str
    name: str
    duration: int
    remaining: int
    status: str
    created_at: str


class TimerHistoryItem(BaseModel):
    id: str
    name: str
    duration: int
    completed_at: str


class WeightConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str


class WeightConvertResponse(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    result: float


class TimeDifferenceRequest(BaseModel):
    start_time: str
    end_time: str
    format: Optional[str] = "%Y-%m-%d %H:%M:%S"


class TimeDifferenceResponse(BaseModel):
    start_time: str
    end_time: str
    years: int
    months: int
    days: int
    hours: int
    minutes: int
    seconds: int
    total_days: int
    total_hours: int
    total_minutes: int
    total_seconds: int


class CalendarDayInfo(BaseModel):
    year: int
    month: int
    day: int
    weekday: str
    weekday_en: str
    lunar_year: str
    lunar_month: str
    lunar_day: str
    solar_term: Optional[str] = None
    is_holiday: bool = False
    holiday_name: Optional[str] = None
    is_today: bool = False


class CalendarMonthRequest(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None


class CalendarMonthResponse(BaseModel):
    year: int
    month: int
    month_name: str
    days: List[CalendarDayInfo]
    first_day_weekday: int
    total_days: int


class LengthConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str


class LengthConvertResponse(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    result: float


class UrlEncodeRequest(BaseModel):
    url: str
    safe: Optional[str] = ''


class UrlEncodeResponse(BaseModel):
    original: str
    encoded: str


class UrlDecodeRequest(BaseModel):
    url: str


class UrlDecodeResponse(BaseModel):
    original: str
    decoded: str


class YamlValidateRequest(BaseModel):
    yaml_str: str


class YamlValidateResponse(BaseModel):
    valid: bool
    formatted: Optional[str] = None
    error: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
