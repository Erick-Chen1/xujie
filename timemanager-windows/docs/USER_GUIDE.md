# Time Manager Windows Client User Guide

## Overview
The Time Manager Windows client is a high-performance desktop application designed for efficient task and schedule management with minimal server communication.

## Features
- Local-first data processing for instant response
- Offline capability with background synchronization
- Multi-language support (English/中文)
- Performance-optimized UI for large datasets

## System Requirements
- Windows 10/11 (64-bit)
- .NET 8.0 Runtime
- 100MB disk space for local storage
- 2GB RAM recommended

## Installation
1. Download the latest release from the releases page
2. Run the installer (TimeManager-Setup.exe)
3. Follow the installation wizard
4. Launch Time Manager from the Start menu

## Performance Features

### Local-First Architecture
- Instant task and schedule updates using SQLite storage
- Background synchronization with compression
- Automatic conflict resolution
- Typical response times:
  - UI interactions: < 16ms
  - Local data operations: < 10ms
  - Initial startup: < 1s

### Offline Support
- Full functionality without internet connection
- Automatic sync when connection is restored
- Conflict resolution with server version
- Local storage optimization

### Server Load Optimization
- Batched synchronization (max 100 items)
- Compressed data transfer (max 50KB per request)
- Minimum 5-second interval between syncs
- Background processing for network operations

## Usage Guide

### Tasks
1. View tasks in the main window
2. Add new tasks using the "+" button
3. Edit tasks by double-clicking
4. Mark tasks complete with checkbox
5. Tasks are saved instantly locally

### Schedules
1. Access schedules from the navigation menu
2. View calendar in day/week/month modes
3. Create schedules with drag-and-drop
4. Edit by double-clicking events
5. Real-time updates with local storage

### Preferences
1. Open Settings from the menu
2. Configure language (English/中文)
3. Set notification preferences
4. Enable/disable calendar sync
5. Changes apply immediately

### Offline Mode
- Continue working without internet
- Changes sync automatically when online
- Status indicator shows sync state
- Manual sync available in menu

## Troubleshooting

### Sync Issues
1. Check internet connection
2. Verify server status
3. Try manual sync from menu
4. Check sync status in preferences

### Performance
1. Clear local cache if needed
2. Verify disk space availability
3. Check system resources
4. Update to latest version

## Support
For technical support or feature requests:
- Submit issues on GitHub
- Contact support team
- Check documentation updates

## Performance Monitoring
The application includes built-in performance monitoring:
- View sync status in system tray
- Check operation times in logs
- Monitor resource usage
- Track sync statistics

## Best Practices
1. Regular local backups
2. Periodic cache clearing
3. Keep app updated
4. Monitor disk space
5. Check sync status regularly
