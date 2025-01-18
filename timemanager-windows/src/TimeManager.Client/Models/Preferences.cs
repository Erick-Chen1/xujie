using System;
using System.Collections.Generic;
using CommunityToolkit.Mvvm.ComponentModel;

namespace TimeManager.Client.Models
{
    public partial class WorkingHours : ObservableObject
    {
        [ObservableProperty]
        private string start = "09:00";

        [ObservableProperty]
        private string end = "17:00";
    }

    public partial class NotificationPreferences : ObservableObject
    {
        [ObservableProperty]
        private bool email = true;

        [ObservableProperty]
        private bool push = true;

        [ObservableProperty]
        private bool wechat = true;
    }

    public partial class CalendarSync : ObservableObject
    {
        [ObservableProperty]
        private bool google = false;

        [ObservableProperty]
        private bool outlook = false;

        [ObservableProperty]
        private bool apple = false;
    }

    public partial class UserPreferences : ObservableObject
    {
        [ObservableProperty]
        private string? userId;

        [ObservableProperty]
        private string timezone = "UTC";

        [ObservableProperty]
        private string language = "en";

        [ObservableProperty]
        private NotificationPreferences notificationPreferences = new();

        [ObservableProperty]
        private Dictionary<string, WorkingHours> workingHours = new()
        {
            { "monday", new WorkingHours() },
            { "tuesday", new WorkingHours() },
            { "wednesday", new WorkingHours() },
            { "thursday", new WorkingHours() },
            { "friday", new WorkingHours() }
        };

        [ObservableProperty]
        private CalendarSync calendarSync = new();
    }
}
