
module.exports = function (controller) {

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
