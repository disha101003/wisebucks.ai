const request =require('request');
let TDKEY = '6ba2569ccfa9403fae1b749ccaabe8d1';


async function CurrentPrices(tickers) //async to load data
{

    
    // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
   let tdurl = 'https://api.twelvedata.com/price?symbol=' + tickers.toString() + '&apikey=' + TDKEY;
    // what to string is doing is if given ["IBM", "FB"] it gives "IBM", "FB"
    
    request.get({
        url: tdurl,
        json: true,
        headers: {'User-Agent': 'request'}
      }, (err, res, data) => {
        if (err) {
          console.log('Error:', err);
        } 
        else if (res.statusCode !== 200) {
          console.log('Status:', res.statusCode);
        } 
        else {
          // data is successfully parsed as a JSON object:
          console.log(data);

          let reformattedData = {};

          if(tickers.length == 1){
            let key = tickers[0]
            reformattedData[key] = parseFloat(data.price);
          } 
          else if (tickers.length > 1){
            for (let key in data) {
                reformattedData[key] = parseFloat(data[key].price);
            }
            
          }
          console.log(reformattedData);
        }

        
    });
}

CurrentPrices(["ABNB","META", "AAPL"])

