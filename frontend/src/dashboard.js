let tickers = ["AAPL", "ACN", "AMZN", "GOOGL", "META", "MSFT", "NFLX", "NVDA", "ORCL", "TSLA", "V", "WMT", "XOM", "ZM"];

var lastPrices = {};
var counter = 15;

function startUpdateCycle() {
    updatePrices();
    setInterval(function() {
        counter--;
        $("#counter").text(counter);
        if (counter <= 0) {
            updatePrices();
            counter = 15;
        }
    }, 1000);
}


$(document).ready(function () {
    tickers.forEach(function (ticker) {
        addTickerToGrid(ticker);
    });
    updateSearch();
    updatePrices();
    startUpdateCycle();
});


function addTickerToGrid(ticker) {
    let htmlData = `
    <div id="${ticker}" class="stock-item">
        <h4 id="${ticker}-name" class="stock-name">${ticker}</h4>
        <h4 id="${ticker}-pct" class="stock-pct"></h4>
        <div class="stock-arrow-container">
            <img class="stock-arrow">
        </div>
        <h4 id="${ticker}-price" class="stock-stock"></h4>
    </div>
    `;
    $("#stocks").append(htmlData);
}


function updatePrices() {
    tickers.forEach(function (ticker) {
        $.ajax({
            url: '/get_stock_data',
            type: 'POST',
            data: JSON.stringify({ ticker: ticker }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function (data) {
                var changePercent = ((data.currentPrice - data.openPrice) / data.openPrice * 100)
                var colorClass;
                if (changePercent <= -2) {
                    colorClass = 'dark-red'
                } else if (changePercent < 0) {
                    colorClass = 'red'
                } else if (changePercent == 0) {
                    colorClass = 'gray'
                } else if (changePercent <= 2) {
                    colorClass = 'green'
                } else {
                    colorClass = 'dark-green'
                }

                $(`#${ticker}-price`).text(`${data.currentPrice.toFixed(2)}`);
                $(`#${ticker}-pct`).text(`${changePercent.toFixed(2)}%`);

                // Remove the color classes from the price as it should not change color
                $(`#${ticker}-price`).removeClass('dark-red red gray green dark-green');

                // Apply the color classes to the percentage and the ticker name
                $(`#${ticker}-pct, #${ticker}-name`).removeClass('dark-red red gray green dark-green').addClass(colorClass);

                var flashClass, arrowClass;
                if (lastPrices[ticker] > data.currentPrice) {
                    flashClass = 'red-flash';
                    arrowClass = 'stock-arrow-red';
                } else if (lastPrices[ticker] < data.currentPrice) {
                    flashClass = 'green-flash';
                    arrowClass = 'stock-arrow-green';
                } else {
                    flashClass = 'gray-flash';
                    arrowClass = 'stock-arrow-dash';
                }
                lastPrices[ticker] = data.currentPrice;

                $(`#${ticker} img`).removeClass('stock-arrow-red stock-arrow-green stock-arrow-dash').addClass(arrowClass);
                $(`#${ticker}`).addClass(flashClass);
                setTimeout(function () {
                    $(`#${ticker}`).removeClass(flashClass);
                }, 1000);


            }
        });
    });
}


document.getElementById("chat-input").addEventListener("input", function() {
    updateSearch();
})


function updateSearch() {
    let items = document.querySelector('.stocks-container');
    while (items.firstChild) items.removeChild(items.firstChild);
    let search = document.getElementById("chat-input").value;
    let newTickers = [];
    tickers.forEach(function(ticker) {
        if (ticker.toLowerCase().includes(search.toLowerCase())) {
            newTickers.push(ticker);
        }
    });
    console.log(newTickers);
    newTickers.forEach(function(ticker) {
        addTickerToGrid(ticker);
    });
    updatePrices();
}