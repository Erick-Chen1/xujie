using Microsoft.Extensions.DependencyInjection;
using System.Windows;

namespace TimeManager.Client
{
    public partial class App : Application
    {
        private ServiceProvider? serviceProvider;

        public App()
        {
            var services = new ServiceCollection();
            ConfigureServices(services);
            serviceProvider = services.BuildServiceProvider();
        }

        private void ConfigureServices(IServiceCollection services)
        {
            // Register services for dependency injection
            services.AddSingleton<MainWindow>();
            // Add other services here
        }

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            var mainWindow = serviceProvider?.GetService<MainWindow>();
            mainWindow?.Show();
        }
    }
}
