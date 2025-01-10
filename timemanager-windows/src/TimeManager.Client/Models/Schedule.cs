using System;
using CommunityToolkit.Mvvm.ComponentModel;

namespace TimeManager.Client.Models
{
    public partial class Schedule : ObservableObject
    {
        [ObservableProperty]
        private string title = string.Empty;

        [ObservableProperty]
        private string description = string.Empty;

        [ObservableProperty]
        private DateTime startTime;

        [ObservableProperty]
        private DateTime endTime;

        [ObservableProperty]
        private string location = string.Empty;
    }
}
