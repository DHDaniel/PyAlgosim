
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
