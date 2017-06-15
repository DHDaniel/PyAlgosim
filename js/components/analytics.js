
module.exports = function (controller) {

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

  analyticsScene.setTween(analyticsTimeline).addIndicators({"name": "bar graph animation"}).addTo(controller);
}
