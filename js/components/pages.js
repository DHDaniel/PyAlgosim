
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
