from typing import Dict, Optional
from pydantic import BaseModel, Field, validator
from datetime import time

class WorkingHours(BaseModel):
    start: str = Field(..., description="Start time in HH:mm format")
    end: str = Field(..., description="End time in HH:mm format")

    @validator("start", "end")
    def validate_time_format(cls, v):
        try:
            hour, minute = map(int, v.split(":"))
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise ValueError
            return v
        except:
            raise ValueError("Time must be in HH:mm format")

class NotificationPreferences(BaseModel):
    email: bool = True
    push: bool = True
    wechat: bool = True

class CalendarSync(BaseModel):
    google: bool = False
    outlook: bool = False
    apple: bool = False

class UserPreferences(BaseModel):
    user_id: Optional[str] = None
    timezone: str = "UTC"
    language: str = "en"
    notification_preferences: NotificationPreferences = Field(
        default_factory=NotificationPreferences
    )
    working_hours: Dict[str, WorkingHours] = Field(
        default_factory=lambda: {
            "monday": WorkingHours(start="09:00", end="17:00"),
            "tuesday": WorkingHours(start="09:00", end="17:00"),
            "wednesday": WorkingHours(start="09:00", end="17:00"),
            "thursday": WorkingHours(start="09:00", end="17:00"),
            "friday": WorkingHours(start="09:00", end="17:00")
        }
    )
    calendar_sync: CalendarSync = Field(default_factory=CalendarSync)

    @validator("language")
    def validate_language(cls, v):
        if v not in ["en", "zh"]:
            raise ValueError("Language must be either 'en' or 'zh'")
        return v
