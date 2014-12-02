// AUTHOR: SEONGTAEK LIM (seongtaek.lim0730@gmail.com)

$(document).ready(function() {
  // START
  var chart = c3.generate({
    bindto: '#bb-chart',
    data: bikeBitData["data"]
  });
  // END
});
