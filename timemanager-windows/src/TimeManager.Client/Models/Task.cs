using System;
using CommunityToolkit.Mvvm.ComponentModel;

namespace TimeManager.Client.Models
{
    public partial class Task : ObservableObject
    {
        [ObservableProperty]
        private string title = string.Empty;

        [ObservableProperty]
        private string description = string.Empty;

        [ObservableProperty]
        private DateTime dueDate;

        [ObservableProperty]
        private TaskPriority priority;

        [ObservableProperty]
        private TaskStatus status;
    }

    public enum TaskPriority
    {
        Low,
        Medium,
        High
    }

    public enum TaskStatus
    {
        NotStarted,
        InProgress,
        Completed
    }
}
