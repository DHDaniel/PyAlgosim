/*======================
HELPER FUNCTIONS
=======================*/

function genRandomRange(num, range) {
  // generates a random number around the range specified of that number. E.g if num = 10 and range = 5, it will return a random number between 5 and 15
  var max = range;
  var min = -range;
  var newNum = num + (Math.random() * (max - min) + min);
  return newNum.toFixed(2);
}

function getDirectionColour(oldPrice, newPrice) {
  // generates the 'direction' color - if it is falling, red, if it is rising, green.
  if ( (oldPrice - newPrice) < 0) {
    return "#ff5252"; // red for negative
  } else {
    return "#00e676"; // green for positive
  }
}

/*========================
Ticker screen animation
=======================*/
var $tickerTable = $("#tickers table");
var $prices = $tickerTable.find(".price");
var $bids = $tickerTable.find(".bid");
var $asks = $tickerTable.find(".ask");
var $volumes = $tickerTable.find(".vol");
var itemsToChange = [$prices, $bids, $asks];
var tl = new TimelineLite();

// self-executing function taking care of changing ticker quotes.
// for some reason, it speeds up and out of control with time.
(function loop() {
  var rand = Math.round(Math.random() * (2000 - 700)) + 700;
  setTimeout(function() {
    // randomly select category
    var $category = itemsToChange[Math.floor(Math.random() * itemsToChange.length)];
    // randomly select cell
    var $cell = $( $category[Math.floor(Math.random() * $category.length)] );

    var number = parseFloat($cell.html());
    var newValue = genRandomRange(number, number * 0.01 );
    var colour = getDirectionColour(number, newValue);


    $cell.html(newValue);
    tl.to($cell, 0.2, {color: "#000000", "background-color": "#f2f2f2"})
      .to($cell, 0.3, {color: colour, "background-color": "transparent"});
    loop();
  }, rand);
}());
