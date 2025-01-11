using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using TimeManager.Client.Models;
using TimeManager.Client.Services;
using TaskModel = TimeManager.Client.Models.Task;

namespace TimeManager.Client.ViewModels
{
    public partial class ScheduleViewModel : ObservableObject
    {
        private readonly LocalStorageService _localStorage;
        private readonly SyncService _syncService;

        [ObservableProperty]
        private ObservableCollection<Schedule> schedules = new();

        [ObservableProperty]
        private Schedule? selectedSchedule;

        [ObservableProperty]
        private bool isLoading;

        public ScheduleViewModel(LocalStorageService localStorage, SyncService syncService)
        {
            _localStorage = localStorage;
            _syncService = syncService;
            _ = LoadSchedulesCommand.ExecuteAsync(null);
        }

        [RelayCommand]
        private async Task LoadSchedulesAsync()
        {
            try
            {
                IsLoading = true;
                // Load from local storage first
                var localSchedules = await _localStorage.GetSchedulesAsync();
                Schedules = new ObservableCollection<Schedule>(localSchedules);

                // Then sync with server in background
                await _syncService.SyncSchedules();
            }
            finally
            {
                IsLoading = false;
            }
        }

        [RelayCommand]
        private async Task AddScheduleAsync(Schedule schedule)
        {
            // Save locally first
            await _localStorage.AddScheduleAsync(schedule);
            Schedules.Add(schedule);

            // Queue for sync
            await _syncService.QueueChange(SyncOperation.Add, schedule);
        }

        [RelayCommand]
        private async Task UpdateScheduleAsync(Schedule schedule)
        {
            // Update locally first
            await _localStorage.UpdateScheduleAsync(schedule);
            var index = Schedules.IndexOf(schedule);
            if (index != -1)
            {
                Schedules[index] = schedule;
            }

            // Queue for sync
            await _syncService.QueueChange(SyncOperation.Update, schedule);
        }

        [RelayCommand]
        private async Task DeleteScheduleAsync(Schedule schedule)
        {
            // Delete locally first
            await _localStorage.DeleteScheduleAsync(schedule);
            Schedules.Remove(schedule);

            // Queue for sync
            await _syncService.QueueChange(SyncOperation.Delete, schedule);
        }
    }
}
