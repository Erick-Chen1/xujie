using System;
using System.Threading.Tasks;
using System.Windows.Threading;
using TimeManager.Client.ViewModels;
using Xunit;

namespace TimeManager.Client.Tests.UI
{
    public class UIResponseTests
    {
        private const int UI_RESPONSE_THRESHOLD_MS = 16; // 60 FPS target

        [Fact]
        public async Task TaskList_ScrollPerformance_ShouldMeetTarget()
        {
            var dispatcher = Dispatcher.CurrentDispatcher;
            var storage = new Services.LocalStorageService();
            var sync = new Services.SyncService(storage, "http://localhost:8000");
            var viewModel = new TaskViewModel(storage, sync);

            // Add 1000 tasks for scroll testing
            for (int i = 0; i < 1000; i++)
            {
                viewModel.Tasks.Add(new Models.Task
                {
                    Title = $"Test Task {i}",
                    Description = $"Performance test task {i}",
                    DueDate = DateTime.Now.AddDays(i % 30)
                });
            }

            var startTime = DateTime.Now;
            await dispatcher.InvokeAsync(() =>
            {
                // Simulate scrolling through tasks
                for (int i = 0; i < 100; i++)
                {
                    viewModel.SelectedTask = viewModel.Tasks[i * 10];
                }
            });
            var elapsed = (DateTime.Now - startTime).TotalMilliseconds / 100; // Average time per selection

            Assert.True(elapsed <= UI_RESPONSE_THRESHOLD_MS,
                $"UI scroll response took {elapsed}ms on average, target is {UI_RESPONSE_THRESHOLD_MS}ms");
        }

        [Fact]
        public async Task PreferencesView_UpdatePerformance_ShouldMeetTarget()
        {
            var dispatcher = Dispatcher.CurrentDispatcher;
            var storage = new Services.LocalStorageService();
            var sync = new Services.SyncService(storage, "http://localhost:8000");
            var localization = new Services.LocalizationService();
            var viewModel = new PreferencesViewModel(storage, sync, localization);

            var startTime = DateTime.Now;
            await dispatcher.InvokeAsync(() =>
            {
                // Simulate rapid preference changes
                for (int i = 0; i < 10; i++)
                {
                    viewModel.Preferences.Language = i % 2 == 0 ? "en" : "zh";
                    viewModel.Preferences.NotificationPreferences.Email = !viewModel.Preferences.NotificationPreferences.Email;
                    viewModel.Preferences.NotificationPreferences.Push = !viewModel.Preferences.NotificationPreferences.Push;
                }
            });
            var elapsed = (DateTime.Now - startTime).TotalMilliseconds / 10; // Average time per update

            Assert.True(elapsed <= UI_RESPONSE_THRESHOLD_MS,
                $"Preferences update took {elapsed}ms on average, target is {UI_RESPONSE_THRESHOLD_MS}ms");
        }
    }
}
