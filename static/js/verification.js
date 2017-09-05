$(document).ready(function() {
  var loadedboxes = $(':checkbox:checked');
  if (loadedboxes.length > 0){
    $("#Submit").prop("disabled", false);
    $("#Submit").prop("value", "LETS FIND A FUCKING GAME TO RUN");
  }
  else
  {
    $("#Submit").prop("disabled", true);
    $("#Submit").prop("value", "SELECT A FUCKING CONSOLE");
  }
  $(":checkbox").change(function() {
    var num = $(':checkbox:checked');
    if (num.length > 0){
      $("#Submit").prop("disabled", false);
      $("#Submit").prop("value", "LETS FIND A FUCKING GAME TO RUN");
    }
    else
    {
      $("#Submit").prop("disabled", true);
      $("#Submit").prop("value", "SELECT A FUCKING CONSOLE");
    }
  });
});
