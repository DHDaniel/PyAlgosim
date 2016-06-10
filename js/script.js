$(document).ready( function () {
  $(".button-collapse").sideNav();

  // for updating the copyright notice
  var date = new Date();
  currentYear = date.getFullYear();
  msg = "Copyright Daniel Hernandez H. " + currentYear + ", under the <a class='white-text' href='https://opensource.org/licenses/MIT'>MIT License</a>";

  $("#copyright-notice").html(msg);
});
