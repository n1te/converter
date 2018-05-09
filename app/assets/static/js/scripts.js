$(document).ready(function() {

  function displayError() {
    $('#converter').hide();
    $('#error').show();
  }

  $.ajax('symbols.json').done(function(data) {
    var i = 0;
    $.each(data, function(key, value) {
      $('#curr1').append($('<option></option>').attr('value', key).text(value));
      $('#curr2').append($('<option></option>').attr('value', key).text(value));
      if (i == 1) {
        $('#curr2').val(key);
      }
      i++;
    });

    $.ajax('rates.json').done(function(data) {
      function convert() {
        if ($('#curr1').val() == $('#curr2').val()) {
            $('#result').val(parseFloat($('#val').val()).toFixed(2));
        }
        else {
            $('#result').val(($('#val').val() * data[$('#curr1').val()][$('#curr2').val()]).toFixed(2));
        }
      }

      convert();
      $('#val').on("paste keyup", function() {
        $(this).val($(this).val().replace(/[^0-9\.]/g,''));
        convert();
      });
      $('#curr1,#curr2').change(function() {
        convert();
      });
    });

  })
});