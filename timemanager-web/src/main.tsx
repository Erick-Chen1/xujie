import { StrictMode, Suspense, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { I18nextProvider } from 'react-i18next'
import './index.css'
import i18n from './i18n'
import App from './App.tsx'

// Wrap App component to ensure i18n is initialized
const AppWrapper = () => {
  useEffect(() => {
    // Force i18n to initialize and load resources
    i18n.init();
  }, []);

  return (
    <Suspense fallback="Loading...">
      <App />
    </Suspense>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <I18nextProvider i18n={i18n}>
      <AppWrapper />
    </I18nextProvider>
  </StrictMode>,
);
