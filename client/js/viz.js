// AUTHOR: SEONGTAEK LIM (seongtaek.lim0730@gmail.com)

$(document).ready(function() {
  // START
  var chart = c3.generate({
    bindto: '#bb-chart',
    data: bikeBitData["data"]
  });

  $("#bb-totalDist").html(bikeBitData["totalD"].toPrecision(4) + " " + bikeBitData["unitD"]);
  $("#bb-maxV").html(bikeBitData["maxInstV"].toPrecision(4) + " " + bikeBitData["unitV"]);
  $("#bb-avgV").html(bikeBitData["avgInstV"].toPrecision(4) + " " + bikeBitData["unitV"]);
  // END
});
