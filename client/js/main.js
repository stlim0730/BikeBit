$(document).ready(function() {

  init();

  // START FILE UPLOAD MODULE
  $("#uploadFile").on("change", function(e) {
    var uploadFileInput = dom($("#uploadFile"));
    var file = uploadFileInput.files;
    var fileName = $("#uploadFile").val();
    $("#uploadForm").submit();
  });
  // END FILE UPLOAD MODULE

});
