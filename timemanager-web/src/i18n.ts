import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './locales/en.json';
import zh from './locales/zh.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      zh: { translation: zh }
    },
    lng: 'en', // Default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false // React already escapes by default
    },
    // Other options
    returnNull: false,
    returnEmptyString: false,
    returnObjects: true,
    saveMissing: true, // Useful for development
    debug: process.env.NODE_ENV === 'development'
  });

export default i18n;
