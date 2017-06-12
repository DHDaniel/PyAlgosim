(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){

// function to animate clock, takes in the global "controller" variable

module.exports = function (controller) {

  // Clock animation for page

  var $wrapper = $("#first-wrapper");
  var $clockContainer = $("#time");
  var $clock = $("#clock");
  var $minutehand = $("#minutehand");
  var $hourhand = $("#hourhand");
  var $backtestingText = $("#backtesting");

  // scene for clock
  var clockScene = new ScrollMagic.Scene({
    triggerElement: "#clock-image-container",
    reverse: false
  });

  // timeline
  var clockTimeline = new TimelineMax({
    // uses jQuery to add word "done" at the end
    onComplete: function () {
    $backtestingText.html("Backtesting done.");
    }
  });

  var clockAnimationDuration = 3.5;

  // tween to animate dots.
  var textTween = TweenMax.to($backtestingText.find("span"), 0.5, {"color": "#00e676"}).repeat(clockAnimationDuration / 0.5).yoyo(true);


  // tweens to animate clock
  clockTimeline
                // rotate minute hand
                .to($minutehand, clockAnimationDuration,   {rotation: 360 * 12, transformOrigin: "50% 100%", ease: Power3.easeInOut})
                // rotate hour hand
                .to($hourhand, clockAnimationDuration, {rotation: 360, transformOrigin: "50% 100%", ease: Power3.easeInOut}, 0)
                // animate backtest text
                .add(textTween, 0)
                // reveal text
                .to($clockContainer, 1, {width: "50%"})
                .to($wrapper.find(".separator"), 1, {width: "80%"});

  clockScene.setTween(clockTimeline).addIndicators({"name" : "clock animation"}).addTo(controller);
}

},{}],2:[function(require,module,exports){

var $nav = $("#navbar");
$(window).scroll(function() {
  if ($(window).scrollTop() != 0) {
    $nav.addClass("active");
  } else {
    $nav.removeClass("active");
  }
});

},{}],3:[function(require,module,exports){
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

},{}],4:[function(require,module,exports){


$(window).load(function() {

  // initializing scroll controller to add effects to.
  var controller = new ScrollMagic.Controller();

  require("./components/terminal.js");

  require("./components/navbar.js");

  require("./components/clock.js")(controller);

});

},{"./components/clock.js":1,"./components/navbar.js":2,"./components/terminal.js":3}]},{},[4]);
