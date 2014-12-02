// AUTHOR: SEONGTAEK LIM (seongtaek.lim0730@gmail.com)

$(document).ready(function() {

  init();

  // START FILE UPLOAD MODULE
  // START VERIFYING DIAMETER INPUT
  $("#diameterInput").keyup(function(e) {
    var value = parseInt($("#diameterInput").val());
    if(isNaN(value)) {
      readyToUpload = false;
      $("#uploadFileDiv").addClass("disabled");
    }
    else {
      readyToUpload = true;
      $("#uploadFileDiv").removeClass("disabled");
    }
  });
  // END VERIFYING DIAMETER INPUT

  // START SUBMITTING FORM VALUES
  $("#uploadFile").on("change", function(e) {
    var uploadFileInput = dom($("#uploadFile"));
    var file = uploadFileInput.files;
    var fileName = $("#uploadFile").val();
    $("#uploadForm").submit();
  });
  // END SUBMITTING FORM VALUES
  // END FILE UPLOAD MODULE
});
