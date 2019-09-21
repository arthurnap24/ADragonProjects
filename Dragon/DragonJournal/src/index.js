import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.min.css'
import './index.css';
// import App from './App';
import Calculator from './App';
import * as serviceWorker from './serviceWorker';

// const lakeList = [
//     {id: 1, name: "Echo Lake", trailhead: "Echo Lake"},
//     {id: 2, name: "Maud Lake", trailhead: "Wright's Lake"},
//     {id: 3, name: "Cascade Lake", trailhead: "Bayview"}
// ]

// var APP_CONSTANTS = {
//     MAX_ACCOUNT_SIZE: 5000000000,
//     MAX_RISK_PER_TRADE_PERCENT: 100,
//     MAX_RETURN_ON_ACCOUNT_SIZE: 100
// }

// ReactDOM.render(<App lakes={lakeList}/>, document.getElementById('root'));
ReactDOM.render( <Calculator />, document.getElementById( 'root' ) );

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
