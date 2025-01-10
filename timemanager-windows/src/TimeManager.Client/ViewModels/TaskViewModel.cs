using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using TimeManager.Client.Models;
using TimeManager.Client.Services;

namespace TimeManager.Client.ViewModels
{
    public partial class TaskViewModel : ObservableObject
    {
        private readonly LocalStorageService _localStorage;
        private readonly SyncService _syncService;

        [ObservableProperty]
        private ObservableCollection<Models.Task> tasks = new();

        [ObservableProperty]
        private Models.Task? selectedTask;

        [ObservableProperty]
        private bool isLoading;

        public TaskViewModel(LocalStorageService localStorage, SyncService syncService)
        {
            _localStorage = localStorage;
            _syncService = syncService;
            LoadTasksCommand.Execute(null);
        }

        [RelayCommand]
        private async Task LoadTasks()
        {
            try
            {
                IsLoading = true;
                // Load from local storage first for immediate response
                var localTasks = await _localStorage.GetTasksAsync();
                Tasks = new ObservableCollection<Models.Task>(localTasks);

                // Then sync with server in background
                await _syncService.SyncTasks();
            }
            finally
            {
                IsLoading = false;
            }
        }

        [RelayCommand]
        private async Task AddTask(Models.Task task)
        {
            // Save locally first
            await _localStorage.AddTaskAsync(task);
            Tasks.Add(task);

            // Queue for sync
            await _syncService.QueueChange(SyncOperation.Add, task);
        }

        [RelayCommand]
        private async Task UpdateTask(Models.Task task)
        {
            // Update locally first
            await _localStorage.UpdateTaskAsync(task);
            var index = Tasks.IndexOf(task);
            if (index != -1)
            {
                Tasks[index] = task;
            }

            // Queue for sync
            await _syncService.QueueChange(SyncOperation.Update, task);
        }

        [RelayCommand]
        private async Task DeleteTask(Models.Task task)
        {
            // Delete locally first
            await _localStorage.DeleteTaskAsync(task);
            Tasks.Remove(task);

            // Queue for sync
            await _syncService.QueueChange(SyncOperation.Delete, task);
        }
    }
}
