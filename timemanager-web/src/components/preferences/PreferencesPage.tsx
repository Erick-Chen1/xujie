import React from 'react';
import { useTranslation } from 'react-i18next';

const PreferencesPage: React.FC = () => {
  const { i18n, t } = useTranslation();

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    i18n.changeLanguage(e.target.value);
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">{t('preferences.title')}</h2>
      <div className="bg-white shadow rounded-lg p-6">
        <div className="mb-4">
          <h3 className="text-lg font-semibold mb-2">{t('preferences.language.title')}</h3>
          <select
            value={i18n.language}
            onChange={handleLanguageChange}
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="en">{t('preferences.language.en')}</option>
            <option value="zh">{t('preferences.language.zh')}</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default PreferencesPage;
