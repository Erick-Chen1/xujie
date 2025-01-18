using System;
using System.Diagnostics;
using System.Threading.Tasks;
using TimeManager.Client.Services;
using TimeManager.Client.ViewModels;
using Xunit;

namespace TimeManager.Client.Tests.Performance
{
    public class PerformanceTests
    {
        private const int STARTUP_TIME_MS = 1000; // 1 second target
        private const int UI_RESPONSE_MS = 16;    // 60 FPS target
        private const int LOCAL_READ_MS = 5;      // Local read target
        private const int LOCAL_WRITE_MS = 10;    // Local write target
        private const int SYNC_TIME_MS = 100;     // Background sync target

        [Fact]
        public async Task LocalStorage_ReadPerformance_ShouldMeetTarget()
        {
            // Arrange
            var storage = new LocalStorageService();
            var stopwatch = new Stopwatch();

            // Act
            stopwatch.Start();
            var tasks = await storage.GetTasksAsync();
            stopwatch.Stop();

            // Assert
            Assert.True(stopwatch.ElapsedMilliseconds <= LOCAL_READ_MS, 
                $"Local read took {stopwatch.ElapsedMilliseconds}ms, target is {LOCAL_READ_MS}ms");
        }

        [Fact]
        public async Task LocalStorage_WritePerformance_ShouldMeetTarget()
        {
            // Arrange
            var storage = new LocalStorageService();
            var task = new Models.Task 
            { 
                Title = "Test Task",
                Description = "Performance Test",
                DueDate = DateTime.Now.AddDays(1)
            };
            var stopwatch = new Stopwatch();

            // Act
            stopwatch.Start();
            await storage.AddTaskAsync(task);
            stopwatch.Stop();

            // Assert
            Assert.True(stopwatch.ElapsedMilliseconds <= LOCAL_WRITE_MS,
                $"Local write took {stopwatch.ElapsedMilliseconds}ms, target is {LOCAL_WRITE_MS}ms");
        }

        [Fact]
        public async Task SyncService_BatchSync_ShouldMeetTarget()
        {
            // Arrange
            var storage = new LocalStorageService();
            var sync = new SyncService(storage, "http://localhost:8000");
            var stopwatch = new Stopwatch();

            // Act
            stopwatch.Start();
            await sync.SyncChanges();
            stopwatch.Stop();

            // Assert
            Assert.True(stopwatch.ElapsedMilliseconds <= SYNC_TIME_MS,
                $"Sync took {stopwatch.ElapsedMilliseconds}ms, target is {SYNC_TIME_MS}ms");
        }

        [Fact]
        public void TaskViewModel_UIUpdate_ShouldMeetTarget()
        {
            // Arrange
            var storage = new LocalStorageService();
            var sync = new SyncService(storage, "http://localhost:8000");
            var viewModel = new TaskViewModel(storage, sync);
            var stopwatch = new Stopwatch();

            // Act
            stopwatch.Start();
            viewModel.Tasks.Add(new Models.Task 
            { 
                Title = "Performance Test Task",
                Description = "Testing UI update performance",
                DueDate = DateTime.Now.AddDays(1)
            });
            stopwatch.Stop();

            // Assert
            Assert.True(stopwatch.ElapsedMilliseconds <= UI_RESPONSE_MS,
                $"UI update took {stopwatch.ElapsedMilliseconds}ms, target is {UI_RESPONSE_MS}ms");
        }
    }
}
