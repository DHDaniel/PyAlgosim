
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
