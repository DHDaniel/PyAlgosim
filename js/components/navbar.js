
var $nav = $("#navbar");
$(window).scroll(function() {
  if ($(window).scrollTop() != 0) {
    $nav.addClass("active");
  } else {
    $nav.removeClass("active");
  }
});
