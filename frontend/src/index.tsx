import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom'
import { store } from './store';
import { Provider } from 'react-redux';
import PreloadData from './components/common/preloadData';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const initializeApp = () => {
  root.render(
    <BrowserRouter>
      <Provider store={store}>
        <PreloadData>
          <App />
        </PreloadData>
      </Provider>
    </BrowserRouter>
  );
};

initializeApp();