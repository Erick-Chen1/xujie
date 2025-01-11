using System;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using TimeManager.Client.Models;
using TimeManager.Client.Services;
using TaskModel = TimeManager.Client.Models.Task;
using SystemTask = System.Threading.Tasks.Task;

namespace TimeManager.Client.ViewModels
{
    public partial class PreferencesViewModel : ObservableObject
    {
        private readonly LocalStorageService _localStorage;
        private readonly SyncService _syncService;
        private readonly LocalizationService _localization;

        [ObservableProperty]
        private UserPreferences preferences;

        [ObservableProperty]
        private bool isSaving;

        public PreferencesViewModel(
            LocalStorageService localStorage,
            SyncService syncService,
            LocalizationService localization)
        {
            _localStorage = localStorage;
            _syncService = syncService;
            _localization = localization;
            preferences = new UserPreferences();
            _ = LoadPreferencesCommand.ExecuteAsync(null);
        }

        [RelayCommand]
        public async SystemTask LoadPreferencesAsync()
        {
            // Load from local storage first
            var localPrefs = await _localStorage.GetPreferencesAsync();
            if (localPrefs != null)
            {
                Preferences = localPrefs;
            }

            // Then sync with server in background
            await _syncService.SyncPreferences();
        }

        [RelayCommand]
        public async SystemTask SavePreferencesAsync()
        {
            try
            {
                IsSaving = true;
                // Save locally first
                await _localStorage.SavePreferencesAsync(Preferences);

                // Apply language change immediately
                _localization.SetLanguage(Preferences.Language);

                // Queue for sync
                await _syncService.QueueChange(SyncOperation.Update, Preferences);
            }
            finally
            {
                IsSaving = false;
            }
        }
    }
}
