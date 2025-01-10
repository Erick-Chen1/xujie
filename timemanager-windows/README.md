# TimeManager Windows Client

## Development Environment Requirements

### Required Software
- Windows 10/11
- Visual Studio 2022 (recommended) or Visual Studio Code with .NET development workload
- .NET SDK 8.0 or later
- Git for Windows

### Performance Optimization Settings
- Enable Native AOT compilation for minimal startup time and memory usage
- Use Windows native APIs for system integration
- Implement local caching to minimize server requests
- Configure release builds with optimization flags

## Project Structure
```
TimeManager.Client/
├── src/
│   ├── TimeManager.Client/           # Main WPF application
│   │   ├── ViewModels/              # MVVM view models
│   │   ├── Models/                  # Business logic models
│   │   ├── Services/                # Application services
│   │   └── Utils/                   # Utility classes
│   └── TimeManager.Client.Tests/    # Unit tests
└── docs/                            # Documentation
```

## Setup Instructions (Windows Development Environment)

1. Install Prerequisites
   - Install Visual Studio 2022 with .NET Desktop Development workload
   - Install .NET SDK 8.0 or later
   - Install Git for Windows

2. Clone and Setup
   ```bash
   git clone https://github.com/Erick-Chen1/xujie.git
   cd xujie/timemanager-windows
   ```

3. Create WPF Project (on Windows)
   ```bash
   dotnet new wpf --name TimeManager.Client
   dotnet new mstest --name TimeManager.Client.Tests
   dotnet new sln --name TimeManagerWindows
   dotnet sln add src/TimeManager.Client/TimeManager.Client.csproj
   dotnet sln add src/TimeManager.Client.Tests/TimeManager.Client.Tests.csproj
   ```

## Development Guidelines

### Performance Optimization
1. Use local storage for caching
   - Implement SQLite for local data storage
   - Cache frequently accessed data in memory
   - Use background synchronization

2. Minimize Server Communication
   - Batch API requests
   - Implement offline-first architecture
   - Use incremental updates

3. Native Performance Features
   - Enable Native AOT compilation
   - Use Windows native APIs
   - Implement efficient UI virtualization

### Build Configuration
```xml
<PropertyGroup>
    <TargetFramework>net8.0-windows</TargetFramework>
    <PublishAot>true</PublishAot>
    <OptimizationPreference>Speed</OptimizationPreference>
    <EnableTrimming>true</EnableTrimming>
    <RuntimeIdentifier>win-x64</RuntimeIdentifier>
</PropertyGroup>
```

## Testing
- Unit tests for business logic
- Integration tests for API communication
- Performance profiling
