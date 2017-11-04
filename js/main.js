(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){

module.exports = function (controller) {

  try {
    var $wrapper = $("#second-wrapper");
    var $bars = $(".bar");
    var $barContainer = $("#analytics");
    var barArray = [];

    var analyticsScene = new ScrollMagic.Scene({
      triggerElement: "#second-wrapper .slide-out-text h2",
      reverse: false
    });

    var analyticsTimeline = new TimelineMax();

    // getting the display status of the container. If it's on mobile, it isn't displayed, and so we don't want to waste time animating it.
    var display = $barContainer.css("display");

    if (display != "none") {
      for (var i = 0; i < $bars.length; i++) {
        var $bar = $($bars[i]);
        var realHeight = $bar.height();
        $bar.height(0);

        analyticsTimeline.to($bar, 0.5, {height: realHeight, ease: Back.easeOut.config(4)}, "-=0.3");
      }
      analyticsTimeline.to($barContainer, 1, {width: "50%"});
    }

    analyticsTimeline.to($wrapper.find(".separator"), 1, {width: "80%"});

    analyticsScene.setTween(analyticsTimeline).addTo(controller);
  } catch (e) {
    console.error(e);  
  }
}

},{}],2:[function(require,module,exports){

// function to animate clock, takes in the global "controller" variable

module.exports = function (controller) {

  try {
    // Clock animation for page
    var $wrapper = $("#first-wrapper");
    var $clockContainer = $("#time");
    var $clock = $("#clock");
    var $minutehand = $("#minutehand");
    var $hourhand = $("#hourhand");
    var $backtestingText = $("#backtesting");

    // scene for clock
    var clockScene = new ScrollMagic.Scene({
      triggerElement: "#first-wrapper .slide-out-text h2",
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

    // getting the display status of the container. If it's on mobile, it isn't displayed, and so we don't want to waste time animating it.
    var display = $clockContainer.css("display");

    if (display != "none") {
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
    }

    // this is always animated
    clockTimeline.to($wrapper.find(".separator"), 1, {width: "80%"});

    clockScene.setTween(clockTimeline).addTo(controller);
  } catch (e) {
      console.error(e);
  }
}

},{}],3:[function(require,module,exports){

var $nav = $("#navbar");
$(window).scroll(function() {
  if ($(window).scrollTop() != 0) {
    $nav.addClass("active");
  } else {
    $nav.removeClass("active");
  }
});

// Opening and closing the navbar, sliding in from the left.
var isNavOpen = false;
$("#menu-toggle").click(function () {
  var $navList = $nav.find("ul");
  var width = $navList.width();
  if (isNavOpen) {
    TweenMax.to($nav.find("ul"), 0.6, {left: -width, ease: Linear.ease});
  } else {
    TweenMax.to($nav.find("ul"), 0.6, {left: 0, ease: Power3.easeOut});
  }
  isNavOpen = !isNavOpen;
});

},{}],4:[function(require,module,exports){

module.exports = function (controller) {

  const windowWidth = $(window).width();
  // early return if on mobile, because the animation is buggy on there.
  if (windowWidth < 768) {
    console.log("Exiting on mobile...");
    return;
  }

  try {

    var $title = $("#top-banner h1");
    var height = $title.height();

    var titleScene = new ScrollMagic.Scene({
      triggerElement: "#top-banner",
      duration: 300,
      triggerHook: "onLeave"
    });

    var timeline = new TimelineMax();

    timeline.to($title, 1, {"font-size": "0"});

    titleScene.setTween(timeline).addTo(controller);

  } catch (e) {
    console.error(e);
  }
}

},{}],5:[function(require,module,exports){
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

module.exports = function () {

  try {
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
  } catch (e) {
    console.log(e);
  }
}

},{}],6:[function(require,module,exports){

$(window).load(function() {

  // initializing scroll controller to add effects to.
  var controller = new ScrollMagic.Controller();

  require("./components/terminal.js")();

  require("./components/navbar.js");

  require("./components/pages.js")(controller);

  require("./components/clock.js")(controller);

  require("./components/analytics.js")(controller);


  console.log("Should always log.");
});

},{"./components/analytics.js":1,"./components/clock.js":2,"./components/navbar.js":3,"./components/pages.js":4,"./components/terminal.js":5}]},{},[6]);
