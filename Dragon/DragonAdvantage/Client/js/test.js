// 1) Send get request to Flask server, and get the OHLC data json object
// 2) Update Google Chart periodically in a configurable interval setting from the frontend
// 3) Implement buys and sells and profit tracking from the frontend

// Should be received from the Flask server
var currentAccountValue = 6000;
var currentSharePrice = 0;
var executedOrders = {
    "MSFT": {
        symbol: "MSFT",
        buyOrders: [/*Insert order objects here*/],
        sellOrders: [/*Insert order objects here*/]
    }
};
var buyOrders = [
    { 
        forSymbol: "MSFT",
        orderType: "buy", 
        orderSubType: "market",
        sharePrice: 12.55,
        numShares: 10
    },
    {
        forSymbol: "MSFT",
        orderType: "buy", 
        orderSubType: "market",
        sharePrice: 12.55,
        numShares: 12
    }
];

var sellOrders = [
    { 
        forSymbol: "MSFT",
        orderType: "sell",
        orderSubType: "market",
        sharePrice: 12.55,
        numShares: 10
    },
    {
        forSymbol: "MSFT",
        orderType: "sell", 
        orderSubType: "market",
        sharePrice: 12.55,
        numShares: 12
    }
];

var ohlcsPerSymbol = {
}

// Load the charts right away

// Call loadChart through SetInterval which in turn calls
// drawChart
function loadChart() {
    google.charts.load( 'current', { 'packages': [ 'corechart' ] } );
    google.charts.setOnLoadCallback( init );
}

var requestedSymbol = "";
var requestedDate = "";
var updatePeriodMS = 1000;
// Solution for setOnLoadCallback not having the option to pass
// params to its setOnLoadCallback handler.
function init() {
    getCandleSticks( requestedSymbol, requestedDate );
}

var MAX_NUM_CANDLES = 60;
var maxCandlestickIndexToRender = 0;
var requestedSymbolOhlcsData;
var currentNumRequestedBars = 1;
var firstCandleStickRow = 0;
function updateData( ohlcs ) {
    var lim = ohlcs.length;
    if ( currentNumRequestedBars > MAX_NUM_CANDLES ) {
        firstCandleStickRow += 1; // forget the very first candlestick shown
    }

    var currentCandleStick;
    for ( var i=firstCandleStickRow; i<currentNumRequestedBars; i++ ) {
        if ( i >= lim ) {
            console.log( "There are no more candles to show, stopping simulation." );
            stopSimulation();
            return;
        }
        currentCandleStick = setOhlcCandlestickRow( requestedSymbolOhlcsData,
            i % MAX_NUM_CANDLES, 
            ohlcs[ i ][ 0 ],
            ohlcs[ i ][ 1 ],
            ohlcs[ i ][ 2 ],
            ohlcs[ i ][ 3 ],
            ohlcs[ i ][ 4 ]
        );
    }
    currentSharePrice = currentCandleStick[ "close" ];
    document.getElementById( "current_price" ).innerHTML = "Current Price: " + currentSharePrice;

    updateChartInfoDiv( currentCandleStick );

    currentNumRequestedBars += 1;
}

function updateChartInfoDiv( currentCandleStick ) {
    var resultHTML = "<ul>"
                   + "<li>tick: " + currentCandleStick[ "tick" ] + "</li>"
                   + "<li>open: " + currentCandleStick[ "open" ] + "</li>"
                   + "<li>close: " + currentCandleStick[ "close" ] + "</li>"
                   + "<li>low: " + currentCandleStick[ "low" ] + "</li>"
                   + "<li>high: " + currentCandleStick[ "high" ] + "</li>";
    document.getElementById( 'chart_info_div' ).innerHTML = resultHTML;
}

function drawChart( symbol ) {
    console.log( "Updating the chart" );
    var ohlcs = ohlcsPerSymbol[ symbol ][ 'ohlcBars' ];
    // Treat first row as data as well.
    //requestedSymbolOhlcsData = google.visualization.arrayToDataTable( ohlcs[ "ohlcBars" ], true );
    updateData( ohlcs );

    var options = {
        title: "Chart Data",
        legend:'none',
        enableInteractivity: true,
        bar: { groupWidth: '100%' },
        candlestick: {
            fallingColor: { strokeWidth: 0, fill: '#a52714' }, //red
            risingColor: { strokeWidth: 0, fill: '#0f9d58' } //green
        },
        vAxis: {
            title: 'Share Price',
            gridlines: {
                count: 10
            },
            minorGridlines: {
                count: 2
            }
        },
        hAxis: {
            title: 'Tick Number'
        },
        series: { 
            0: { type: 'candlesticks' },
            1: { type: 'lines' }
        }
    };

    var chart = new google.visualization.ComboChart( document.getElementById( 'chart_div' ) );
    chart.draw( requestedSymbolOhlcsData, options );
}

function setOhlcCandlestickRow( requestedSymbolOhlcsData, row, idx, low, open, close, high ) {
    requestedSymbolOhlcsData.setCell( row, 0, idx );
    requestedSymbolOhlcsData.setCell( row, 1, low );
    requestedSymbolOhlcsData.setCell( row, 2, open );
    requestedSymbolOhlcsData.setCell( row, 3, close );
    requestedSymbolOhlcsData.setCell( row, 4, high );
    requestedSymbolOhlcsData.setCell( row, 5, 110 );
    
    return {
        tick: idx,
        open: open,
        close: close,
        low: low,
        high: high,
        movingAverage: 110
    }
}

// function printOrders() {
//     buyLim = buyOrders.length;
//     sellLim = sellOrders.length;
    
//     for ( var i=0; i<buyLim; i++ ) {
//         var forSymbol = buyOrders[i].forSymbol;
//         var orderType = buyOrders[i].orderType;
//         var orderSubType = buyOrders[i].orderSubType;
//         var sharePrice = buyOrders[i].sharePrice;
//         var numShares = buyOrders[i].numShares;

//         var result = JSON.stringify( buyOrders[ i ] );
//         document.getElementById("orders").innerHTML += result;
//     }

//     for ( var i=0; i<sellLim; i++ ) {
//         var forSymbol = sellOrders[i].forSymbol;
//         var orderType = sellOrders[i].orderType;
//         var orderSubType = sellOrders[i].orderSubType;
//         var sharePrice = sellOrders[i].sharePrice;
//         var numShares = sellOrders[i].numShares;

//         var result = JSON.stringify( sellOrders[ i ] );
//         document.getElementById("orders").innerHTML += result;
//     }
// }

var currentShares = 0; // should be per symbol being watched
function buy() {
    var numShares = parseInt( document.getElementById( "shares_to_trade" ).value );
    var totalAmount = numShares * currentSharePrice;
    if ( currentAccountValue > totalAmount ) {
        currentShares += numShares;
        currentAccountValue -= totalAmount;
        //buyOrders.push( createOrder( symbol, "buy", buyType, currentSharePrice, numShares) );
        updateAccountInfo();
        return true;
    }
    return false;
}

// Only support market sells for now.
function sell() {
    var numShares = parseInt( document.getElementById( "shares_to_trade" ).value );
    if ( currentShares >= numShares ) {
        //sellOrders.push( createOrder( symbol, "sell", sellType, currentSharePrice, numShares) );
        currentShares -= numShares;
        currentAccountValue += ( numShares * currentSharePrice );
        updateAccountInfo();
        return true;
    }
    return false;
}

function createOrder( symbol, orderType, orderSubType, sharePrice, numShares ) {
    console.log( "Creating " + orderType + " order for " + symbol );
    return {
        forSymbol: symbol,
        orderType: orderType, 
        orderSubType: orderSubType,
        sharePrice: sharePrice,
        numShares: numShares
    }
}

/* For simulation */
var simulation;
function startSimulation() {
    currentShares = 0;
    requestedSymbol = document.getElementById( "sim_symbol" ).value;
    requestedDate = document.getElementById( "sim_date" ).value;
    updatePeriodMS = parseInt( document.getElementById( "sim_period" ).value );
    currentAccountValue = parseInt( document.getElementById( "sim_account_val" ).value );
    updateAccountInfo();
    console.log( requestedSymbol );
    console.log( requestedDate );
    console.log( updatePeriodMS );
    // requestedSymbol = symbol;
    // requestedDate = date;
    // updatePeriodMS = periodMs;
    loadChart();
}

function updateAccountInfo()  {
    document.getElementById( "account_value" ).innerHTML = "Account Value: " + currentAccountValue;
    document.getElementById( "num_shares" ).innerHTML = "Current Shares: " + currentShares;
}

function stopSimulation() {
    console.log( "stopping simulation" );
    clearInterval( simulation );
    return true;
}

function ohlcJSONToGoogleChartsDataTable( symbol, ohlcs ) {
    var barNum = 0;
    var ohlcsArr = JSON.parse( ohlcs ); // an array of ohlc objects
    var lim = ohlcsArr.length;
    var googleChartDataBars = [];
    var minY = 0;
    var maxY = 0;

    for ( barNum; barNum < lim; barNum++ ) {
        var ohlcObj = ohlcsArr[ barNum ];
        var low = ohlcObj.low;
        var open = ohlcObj.open;
        var close = ohlcObj.close;
        var high = ohlcObj.high;
        var prices = [ low, open, close, high ];

        for ( var i=0; i<prices.length; i++ )
        {
            if ( prices[ i ] > minY ) {
                minY = prices[ i ];
            }
            if ( prices[ i ] > maxY ) {
                maxY = prices[ i ];
            }
        }

        var googleChartDataBar = [ 
            barNum.toString(), low, open, close, high
        ];
        googleChartDataBars.push( googleChartDataBar );
    }
    ohlcsPerSymbol[ symbol ] = { 
        // ohlcBars: googleChartDataBars.slice( 0, 30 ),
        ohlcBars: googleChartDataBars,
        minY: (minY - 2),
        maxY: (maxY + 2)
    };

    return true;
}

// initialize the data table with a maximum number of columns
function initData() {
    requestedSymbolOhlcsData = new google.visualization.DataTable(); // THESE properties should be identified and placed inside an info dictionary that contains per symbol values
    requestedSymbolOhlcsData.addColumn( 'number', 'Candlestick Index' );
    requestedSymbolOhlcsData.addColumn( 'number', 'Low' );
    requestedSymbolOhlcsData.addColumn( 'number', 'Open' );
    requestedSymbolOhlcsData.addColumn( 'number', 'Close' );
    requestedSymbolOhlcsData.addColumn( 'number', 'High' );
    requestedSymbolOhlcsData.addColumn( 'number', 'Moving Average' );
    requestedSymbolOhlcsData.addRows( MAX_NUM_CANDLES );
}

// date must be YYYYMMDD
function getCandleSticks( symbol, date ) {
    console.log( "getCandleSticks is invoked" );
    var ohlcCandles = [];
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if ( this.readyState == 4 && this.status == 200 ) {
            ohlcJSONToGoogleChartsDataTable( symbol, this.responseText );
            console.log( JSON.stringify( ohlcsPerSymbol ) );
            //drawChart( symbol );
            initData();
            drawChart( symbol );
            simulation = setInterval( function() { 
                drawChart( symbol );
                console.log( "update currentShares for all the stocks possible/requested" ) 
            }, 
            updatePeriodMS );
        }
    }
    uri = "http://127.0.0.1:5000/stock/" + symbol + "?date=" + date;
    xhttp.open( "GET", uri, true );
    xhttp.send();
}

