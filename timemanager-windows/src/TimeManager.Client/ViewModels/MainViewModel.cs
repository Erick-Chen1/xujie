using CommunityToolkit.Mvvm.ComponentModel;
using System.Collections.ObjectModel;
using TimeManager.Client.Models;

namespace TimeManager.Client.ViewModels
{
    public partial class MainViewModel : ObservableObject
    {
        [ObservableProperty]
        private ObservableCollection<Task> tasks = new();

        [ObservableProperty]
        private string statusMessage = string.Empty;

        public MainViewModel()
        {
            // Initialize with empty state
            Tasks = new ObservableCollection<Task>();
        }
    }
}
