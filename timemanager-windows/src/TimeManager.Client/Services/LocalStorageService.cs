using Microsoft.Data.Sqlite;
using System.Threading.Tasks;

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

        private async Task InitializeDatabase()
        {
            using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            // Create tables with indices for performance
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
            ";
            await command.ExecuteNonQueryAsync();
        }
    }
}
