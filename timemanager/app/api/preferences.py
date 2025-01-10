from fastapi import APIRouter, Depends
from ..models.preferences import UserPreferences
from ..db.memory_db import db
from .auth import oauth2_scheme
from .schedules import get_current_user_id

router = APIRouter()

@router.put("", response_model=UserPreferences)
async def update_preferences(
    preferences: UserPreferences,
    current_user_id: str = Depends(get_current_user_id)
):
    preferences_dict = preferences.dict()
    preferences_dict["user_id"] = current_user_id
    updated = db.set_preferences(current_user_id, preferences_dict)
    return UserPreferences(**updated)

@router.get("", response_model=UserPreferences)
async def get_preferences(current_user_id: str = Depends(get_current_user_id)):
    prefs = db.get_preferences(current_user_id)
    if not prefs:
        # Return default preferences
        prefs = {
            "user_id": current_user_id,
            "timezone": "UTC",
            "language": "en",  # Default language is English
            "notification_preferences": {
                "email": True,
                "push": True,
                "wechat": True
            },
            "working_hours": {
                "monday": {"start": "09:00", "end": "17:00"},
                "tuesday": {"start": "09:00", "end": "17:00"},
                "wednesday": {"start": "09:00", "end": "17:00"},
                "thursday": {"start": "09:00", "end": "17:00"},
                "friday": {"start": "09:00", "end": "17:00"}
            },
            "calendar_sync": {
                "google": False,
                "outlook": False,
                "apple": False
            }
        }
        db.set_preferences(current_user_id, prefs)
    return UserPreferences(**prefs)
