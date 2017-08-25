$(document).ready(function() {
  $("#Submit").prop("disabled", true);
  $("#Submit").prop("value", "choose a console");
  $(":checkbox").change(function() {
    var num = $(':checkbox:checked');
    if (num.length > 0){
      $("#Submit").prop("disabled", false);
      $("#Submit").prop("value", "submit");
    }
    else
    {
      $("#Submit").prop("disabled", true);
      $("#Submit").prop("value", "choose a console");
    }
  });
});
