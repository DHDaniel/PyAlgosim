
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
