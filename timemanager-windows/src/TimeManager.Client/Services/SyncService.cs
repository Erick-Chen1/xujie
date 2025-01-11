using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Collections.Generic;
using System.Linq;
using TimeManager.Client.Models;
using TaskModel = TimeManager.Client.Models.Task;
using SystemTask = System.Threading.Tasks.Task;

namespace TimeManager.Client.Services
{
    public class SyncService
    {
        private readonly LocalStorageService _localStorage;
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private const int MAX_BATCH_SIZE = 100;
        private const int SYNC_INTERVAL_MS = 5000;

        public SyncService(LocalStorageService localStorage, string baseUrl)
        {
            _localStorage = localStorage;
            _baseUrl = baseUrl;
            _httpClient = new HttpClient { BaseAddress = new Uri(baseUrl) };
        }

        public async SystemTask StartBackgroundSync()
        {
            while (true)
            {
                try
                {
                    await SyncChanges();
                }
                catch (Exception ex)
                {
                    // Log error but continue syncing
                    Console.WriteLine($"Sync error: {ex.Message}");
                }
                await Task.Delay(SYNC_INTERVAL_MS);
            }
        }

        private readonly Queue<(object Entity, SyncOperation Operation)> _syncQueue = new();
        private readonly object _queueLock = new();

        public void QueueChange(object entity, SyncOperation operation)
        {
            lock (_queueLock)
            {
                _syncQueue.Enqueue((entity, operation));
            }
        }

        private async SystemTask SyncChanges()
        {
            try
            {
                await SyncTasks();
                await SyncSchedules();
                await SyncPreferences();
                await ProcessSyncQueue();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error during sync: {ex.Message}");
            }
        }

        private async SystemTask ProcessSyncQueue()
        {
            while (true)
            {
                (object Entity, SyncOperation Operation) change;
                lock (_queueLock)
                {
                    if (!_syncQueue.Any())
                        break;
                    change = _syncQueue.Dequeue();
                }

                try
                {
                    switch (change.Entity)
                    {
                        case TaskModel task:
                            await SyncTaskChange(task, change.Operation);
                            break;
                        case Schedule schedule:
                            await SyncScheduleChange(schedule, change.Operation);
                            break;
                        case Preferences preferences:
                            await SyncPreferencesChange(preferences, change.Operation);
                            break;
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error processing sync change: {ex.Message}");
                }
            }
        }

        private async SystemTask SyncTaskChange(TaskModel task, SyncOperation operation)
        {
            var endpoint = $"/api/tasks";
            try
            {
                switch (operation)
                {
                    case SyncOperation.Add:
                        await _httpClient.PostAsJsonAsync(endpoint, task);
                        break;
                    case SyncOperation.Update:
                        await _httpClient.PutAsJsonAsync($"{endpoint}/{task.Id}", task);
                        break;
                    case SyncOperation.Delete:
                        await _httpClient.DeleteAsync($"{endpoint}/{task.Id}");
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error syncing task change: {ex.Message}");
            }
        }

        private async SystemTask SyncScheduleChange(Schedule schedule, SyncOperation operation)
        {
            var endpoint = $"/api/schedules";
            try
            {
                switch (operation)
                {
                    case SyncOperation.Add:
                        await _httpClient.PostAsJsonAsync(endpoint, schedule);
                        break;
                    case SyncOperation.Update:
                        await _httpClient.PutAsJsonAsync($"{endpoint}/{schedule.Id}", schedule);
                        break;
                    case SyncOperation.Delete:
                        await _httpClient.DeleteAsync($"{endpoint}/{schedule.Id}");
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error syncing schedule change: {ex.Message}");
            }
        }

        private async SystemTask SyncPreferencesChange(UserPreferences preferences, SyncOperation operation)
        {
            var endpoint = $"/api/preferences";
            try
            {
                // Preferences only support updates
                if (operation == SyncOperation.Update)
                {
                    await _httpClient.PutAsJsonAsync(endpoint, preferences);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error syncing preferences change: {ex.Message}");
            }
        }

        public async SystemTask SyncTasks()
        {
            try
            {
                var tasks = await _httpClient.GetFromJsonAsync<List<TaskModel>>("/api/tasks");
                if (tasks != null)
                {
                    await _localStorage.SaveTasksAsync(tasks);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error syncing tasks: {ex.Message}");
            }
        }

        public async SystemTask SyncSchedules()
        {
            try
            {
                var schedules = await _httpClient.GetFromJsonAsync<List<Schedule>>("/api/schedules");
                if (schedules != null)
                {
                    await _localStorage.SaveSchedulesAsync(schedules);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error syncing schedules: {ex.Message}");
            }
        }

        public async SystemTask SyncPreferences()
        {
            try
            {
                var preferences = await _httpClient.GetFromJsonAsync<UserPreferences>("/api/preferences");
                if (preferences != null)
                {
                    await _localStorage.SavePreferencesAsync(preferences);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error syncing preferences: {ex.Message}");
            }
        }
    }
}
