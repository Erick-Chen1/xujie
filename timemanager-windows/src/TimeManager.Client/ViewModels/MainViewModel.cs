using CommunityToolkit.Mvvm.ComponentModel;
using System.Collections.ObjectModel;
using TimeManager.Client.Models;
using TaskModel = TimeManager.Client.Models.Task;

namespace TimeManager.Client.ViewModels
{
    public partial class MainViewModel : ObservableObject
    {
        [ObservableProperty]
        private ObservableCollection<TaskModel> tasks = new();

        [ObservableProperty]
        private string statusMessage = string.Empty;

        public MainViewModel()
        {
            // Initialize with empty state
            Tasks = new ObservableCollection<TaskModel>();
        }
    }
}
