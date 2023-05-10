import React from 'react';
import * as ReactDOM from 'react-dom/client';
import {App} from './components/App'
import {Demo} from './components/Demo'


const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App/>)
