// Type definitions for time-related values
export type TimeString = string; // Format: "HH:mm"
export type DayOfWeek = "monday" | "tuesday" | "wednesday" | "thursday" | "friday";
export type Language = "en" | "zh";

// Validation utilities
export const isValidTimeString = (time: string): boolean => {
  const timeRegex = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
  return timeRegex.test(time);
};

export const isValidDayOfWeek = (day: string): day is DayOfWeek => {
  return ["monday", "tuesday", "wednesday", "thursday", "friday"].includes(day.toLowerCase());
};

export interface WorkingHours {
  start: TimeString;
  end: TimeString;
}

export interface NotificationPreferences {
  email: boolean;
  push: boolean;
  wechat: boolean;
}

export interface CalendarSync {
  google: boolean;
  outlook: boolean;
  apple: boolean;
}

export interface UserPreferences {
  user_id?: string;
  timezone: string;
  language: Language;
  notification_preferences: NotificationPreferences;
  working_hours: { [key in DayOfWeek]: WorkingHours };
  calendar_sync: CalendarSync;
}

// Helper function to get default preferences
export const getDefaultPreferences = (): UserPreferences => ({
  timezone: "UTC",
  language: "en",
  notification_preferences: {
    email: true,
    push: true,
    wechat: true
  },
  working_hours: {
    monday: { start: "09:00", end: "17:00" },
    tuesday: { start: "09:00", end: "17:00" },
    wednesday: { start: "09:00", end: "17:00" },
    thursday: { start: "09:00", end: "17:00" },
    friday: { start: "09:00", end: "17:00" }
  },
  calendar_sync: {
    google: false,
    outlook: false,
    apple: false
  }
});
