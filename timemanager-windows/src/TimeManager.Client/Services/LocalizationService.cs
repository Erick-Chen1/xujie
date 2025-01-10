using System;
using System.Collections.Generic;
using System.Globalization;
using System.Threading;

namespace TimeManager.Client.Services
{
    public class LocalizationService
    {
        private static readonly Dictionary<string, Dictionary<string, string>> _translations = new()
        {
            ["en"] = new Dictionary<string, string>(),
            ["zh"] = new Dictionary<string, string>()
        };

        public void Initialize()
        {
            LoadTranslations();
        }

        public void SetLanguage(string language)
        {
            if (!_translations.ContainsKey(language))
                language = "en";

            Thread.CurrentThread.CurrentUICulture = new CultureInfo(language);
            Thread.CurrentThread.CurrentCulture = new CultureInfo(language);
        }

        private void LoadTranslations()
        {
            // Load translations from embedded resources
            // This will be populated with the same strings as the web client
        }

        public string GetString(string key)
        {
            var currentLanguage = Thread.CurrentThread.CurrentUICulture.TwoLetterISOLanguageName;
            return _translations[currentLanguage].GetValueOrDefault(key, key);
        }
    }
}
