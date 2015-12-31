$("#step1_button").click(function(event) {

      /* stop form from submitting normally */
      event.preventDefault();

      /* get some values from elements on the page: */
      var $form = $("#step1");
      url = $form.attr( 'action' );

      /* Send the data using post */
      var posting = $.get( url, { session_code: $('#session_code').val() } );

      /* Alerts the results */
      posting.done(function( data ) {
        alert('success');
      });
    });

/* attach a submit handler to the form */
    $("#step2_button").click(function(event) {

      /* stop form from submitting normally */
      event.preventDefault();

      /* get some values from elements on the page: */
      var $form = $("#step2");
      url = $form.attr( 'action' );

      /* Send the data using post */
      var posting = $.get( url, { budget: $('#budget').val(), start_date: $('#dpd1').val(), end_date: $("#dpd2").val() } );

      /* Alerts the results */
      posting.done(function( data ) {
        alert('success');
      });
    });

    $.getJSON('https://freegeoip.net/json/') 
     .done (function(location)
     {
          $('#origin').val(location.city + ", " + location.region_code);
     });