using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.IO;
using TimeManager.Client.Models;
using TaskModel = TimeManager.Client.Models.Task;

namespace TimeManager.Client.Services
{
    public class LocalStorageService
    {
        private readonly string connectionString;

        public LocalStorageService()
        {
            var dbPath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "TimeManager",
                "timemanager.db"
            );
            Directory.CreateDirectory(Path.GetDirectoryName(dbPath)!);
            connectionString = $"Data Source={dbPath}";
            InitializeDatabase().Wait();
        }

        private async System.Threading.Tasks.Task InitializeDatabase()
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                CREATE TABLE IF NOT EXISTS Tasks (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Title TEXT NOT NULL,
                    Description TEXT,
                    DueDate TEXT,
                    Priority INTEGER,
                    Status INTEGER,
                    CreatedAt TEXT NOT NULL,
                    UpdatedAt TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_tasks_duedate ON Tasks(DueDate);
                CREATE INDEX IF NOT EXISTS idx_tasks_status ON Tasks(Status);

                CREATE TABLE IF NOT EXISTS Schedules (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Title TEXT NOT NULL,
                    StartTime TEXT NOT NULL,
                    EndTime TEXT NOT NULL,
                    RecurrencePattern TEXT,
                    CreatedAt TEXT NOT NULL,
                    UpdatedAt TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Preferences (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Language TEXT NOT NULL DEFAULT 'en',
                    Theme TEXT NOT NULL DEFAULT 'light',
                    WorkingHours TEXT NOT NULL DEFAULT '09:00-17:00',
                    NotificationEnabled INTEGER NOT NULL DEFAULT 1,
                    LastUpdated TEXT NOT NULL
                );
            ";
            await command.ExecuteNonQueryAsync();
        }

        public async System.Threading.Tasks.Task<List<TaskModel>> GetTasksAsync()
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "SELECT * FROM Tasks ORDER BY DueDate, Priority DESC";

            var tasks = new List<TaskModel>();
            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                tasks.Add(new TaskModel
                {
                    Id = reader.GetInt32(0),
                    Title = reader.GetString(1),
                    Description = reader.IsDBNull(2) ? null : reader.GetString(2),
                    DueDate = reader.IsDBNull(3) ? null : DateTime.Parse(reader.GetString(3)),
                    Priority = reader.GetInt32(4),
                    Status = reader.GetInt32(5),
                    CreatedAt = DateTime.Parse(reader.GetString(6)),
                    UpdatedAt = DateTime.Parse(reader.GetString(7))
                });
            }

            return tasks;
        }

        public async System.Threading.Tasks.Task<List<Schedule>> GetSchedulesAsync()
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "SELECT * FROM Schedules ORDER BY StartTime";

            var schedules = new List<Schedule>();
            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                schedules.Add(new Schedule
                {
                    Id = reader.GetInt32(0),
                    Title = reader.GetString(1),
                    StartTime = DateTime.Parse(reader.GetString(2)),
                    EndTime = DateTime.Parse(reader.GetString(3)),
                    RecurrencePattern = reader.IsDBNull(4) ? null : reader.GetString(4),
                    CreatedAt = DateTime.Parse(reader.GetString(5)),
                    UpdatedAt = DateTime.Parse(reader.GetString(6))
                });
            }

            return schedules;
        }

        public async System.Threading.Tasks.Task<UserPreferences> GetPreferencesAsync()
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "SELECT * FROM Preferences ORDER BY Id DESC LIMIT 1";

            using var reader = await command.ExecuteReaderAsync();
            if (await reader.ReadAsync())
            {
                return new Preferences
                {
                    Id = reader.GetInt32(0),
                    Language = reader.GetString(1),
                    Theme = reader.GetString(2),
                    WorkingHours = reader.GetString(3),
                    NotificationEnabled = reader.GetInt32(4) == 1,
                    LastUpdated = DateTime.Parse(reader.GetString(5))
                };
            }

            return new Preferences();
        }

        public async System.Threading.Tasks.Task AddTaskAsync(TaskModel task)
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                INSERT INTO Tasks (Title, Description, DueDate, Priority, Status, CreatedAt, UpdatedAt)
                VALUES (@Title, @Description, @DueDate, @Priority, @Status, @CreatedAt, @UpdatedAt)";

            command.Parameters.AddWithValue("@Title", task.Title);
            command.Parameters.AddWithValue("@Description", (object?)task.Description ?? DBNull.Value);
            command.Parameters.AddWithValue("@DueDate", (object?)task.DueDate?.ToString("O") ?? DBNull.Value);
            command.Parameters.AddWithValue("@Priority", task.Priority);
            command.Parameters.AddWithValue("@Status", task.Status);
            command.Parameters.AddWithValue("@CreatedAt", DateTime.UtcNow.ToString("O"));
            command.Parameters.AddWithValue("@UpdatedAt", DateTime.UtcNow.ToString("O"));

            await command.ExecuteNonQueryAsync();
        }

        public async System.Threading.Tasks.Task UpdateTaskAsync(TaskModel task)
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                UPDATE Tasks 
                SET Title = @Title, Description = @Description, DueDate = @DueDate,
                    Priority = @Priority, Status = @Status, UpdatedAt = @UpdatedAt
                WHERE Id = @Id";

            command.Parameters.AddWithValue("@Id", task.Id);
            command.Parameters.AddWithValue("@Title", task.Title);
            command.Parameters.AddWithValue("@Description", (object?)task.Description ?? DBNull.Value);
            command.Parameters.AddWithValue("@DueDate", (object?)task.DueDate?.ToString("O") ?? DBNull.Value);
            command.Parameters.AddWithValue("@Priority", task.Priority);
            command.Parameters.AddWithValue("@Status", task.Status);
            command.Parameters.AddWithValue("@UpdatedAt", DateTime.UtcNow.ToString("O"));

            await command.ExecuteNonQueryAsync();
        }

        public async System.Threading.Tasks.Task DeleteTaskAsync(TaskModel task)
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "DELETE FROM Tasks WHERE Id = @Id";
            command.Parameters.AddWithValue("@Id", task.Id);

            await command.ExecuteNonQueryAsync();
        }

        public async System.Threading.Tasks.Task AddScheduleAsync(Schedule schedule)
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                INSERT INTO Schedules (Title, StartTime, EndTime, RecurrencePattern, CreatedAt, UpdatedAt)
                VALUES (@Title, @StartTime, @EndTime, @RecurrencePattern, @CreatedAt, @UpdatedAt)";

            command.Parameters.AddWithValue("@Title", schedule.Title);
            command.Parameters.AddWithValue("@StartTime", schedule.StartTime.ToString("O"));
            command.Parameters.AddWithValue("@EndTime", schedule.EndTime.ToString("O"));
            command.Parameters.AddWithValue("@RecurrencePattern", (object?)schedule.RecurrencePattern ?? DBNull.Value);
            command.Parameters.AddWithValue("@CreatedAt", DateTime.UtcNow.ToString("O"));
            command.Parameters.AddWithValue("@UpdatedAt", DateTime.UtcNow.ToString("O"));

            await command.ExecuteNonQueryAsync();
        }

        public async System.Threading.Tasks.Task UpdateScheduleAsync(Schedule schedule)
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                UPDATE Schedules 
                SET Title = @Title, StartTime = @StartTime, EndTime = @EndTime,
                    RecurrencePattern = @RecurrencePattern, UpdatedAt = @UpdatedAt
                WHERE Id = @Id";


            command.Parameters.AddWithValue("@Id", schedule.Id);
            command.Parameters.AddWithValue("@Title", schedule.Title);
            command.Parameters.AddWithValue("@StartTime", schedule.StartTime.ToString("O"));
            command.Parameters.AddWithValue("@EndTime", schedule.EndTime.ToString("O"));
            command.Parameters.AddWithValue("@RecurrencePattern", (object?)schedule.RecurrencePattern ?? DBNull.Value);
            command.Parameters.AddWithValue("@UpdatedAt", DateTime.UtcNow.ToString("O"));

            await command.ExecuteNonQueryAsync();
        }

        public async System.Threading.Tasks.Task DeleteScheduleAsync(Schedule schedule)
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "DELETE FROM Schedules WHERE Id = @Id";
            command.Parameters.AddWithValue("@Id", schedule.Id);

            await command.ExecuteNonQueryAsync();
        }

        public async System.Threading.Tasks.Task SavePreferencesAsync(UserPreferences preferences)
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                INSERT OR REPLACE INTO Preferences (Id, Language, Theme, WorkingHours, NotificationEnabled, LastUpdated)
                VALUES (@Id, @Language, @Theme, @WorkingHours, @NotificationEnabled, @LastUpdated)";

            command.Parameters.AddWithValue("@Id", preferences.Id);
            command.Parameters.AddWithValue("@Language", preferences.Language);
            command.Parameters.AddWithValue("@Theme", preferences.Theme);
            command.Parameters.AddWithValue("@WorkingHours", preferences.WorkingHours);
            command.Parameters.AddWithValue("@NotificationEnabled", preferences.NotificationEnabled ? 1 : 0);
            command.Parameters.AddWithValue("@LastUpdated", DateTime.UtcNow.ToString("O"));

            await command.ExecuteNonQueryAsync();
        }
    }
}
