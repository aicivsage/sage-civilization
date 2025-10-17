import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { ErrorBoundary } from './components/ErrorBoundary';

// Global error handler to log errors with full details (PROPERLY STRINGIFIED)
window.addEventListener('error', (event) => {
  console.error('========== GLOBAL ERROR CAUGHT ==========');
  console.error('Message:', event.message);
  console.error('File:', event.filename);
  console.error('Line:', event.lineno, 'Col:', event.colno);

  if (event.error) {
    console.error('Error object:', event.error);
    console.error('Error message:', event.error.message);
    console.error('Error name:', event.error.name);
    console.error('Error stack:', event.error.stack);

    // Stringify full error object
    try {
      console.error('Full error JSON:', JSON.stringify(event.error, Object.getOwnPropertyNames(event.error), 2));
    } catch (e) {
      console.error('Could not stringify error:', e);
    }
  }
  console.error('=========================================');
});

// Global unhandled promise rejection handler (PROPERLY STRINGIFIED)
window.addEventListener('unhandledrejection', (event) => {
  console.error('========== UNHANDLED PROMISE REJECTION ==========');
  console.error('Reason:', event.reason);

  if (event.reason) {
    // Check if it's an Error object
    if (event.reason instanceof Error) {
      console.error('Error message:', event.reason.message);
      console.error('Error name:', event.reason.name);
      console.error('Error stack:', event.reason.stack);
    }

    // Try to stringify
    try {
      console.error('Full reason JSON:', JSON.stringify(event.reason, Object.getOwnPropertyNames(event.reason), 2));
    } catch (e) {
      console.error('Could not stringify reason:', e);
      console.error('Reason toString():', String(event.reason));
    }
  }
  console.error('===============================================');
});

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>
);
