function initDateFields() {
	// for all form created by help django_crispy_form
	$("input.dateinput").datetimepicker({
		'format': 'YYYY-MM-DD'
	}).on('dp.hide', function(event){
		$(this).blur();
	});

    //for form exam field data and time
    $("input.datetimeinput").datetimepicker({
		'format': 'DD/MM/YYYY HH:MM:SS'
	}).on('dp.hide', function(event){
		$(this).blur();
	});
    
    //for form students_add
	$("#birthday").datetimepicker({
		'format': 'YYYY-MM-DD'
	}).on('dp.hide', function(event){
		$(this).blur();
	});

	//$("#birthday").val($("#birthday").val() + html(<i class="fa fa-calendar" style="font-size:24px"></i>);

}


function initGroupSelector() {
    // look up select element with groups and atach our even handler 
    // on field "change" event
    $("#group-selector select").change(function(event) {
      // get value of currently selected group option
      var group = $(this).val();

      if(group) {
      	// set cookie expiration date 1 year since now;
      	// cookie creation function takes period in days
      	$.cookie('current_group', group, {'path': '/', 'expires': 365});
      } else {
      	// otherwise we delete the cookie
      	$.removeCookie('current_group', {'path': '/'});
      }

      // and reload a page
      location.reload(true);

      return true;
    });
}

function initJournal() {
    var indicator = $('#ajax-progress-indicator');

	$('.day-box input[type="checkbox"]').click(function(event){
		
		var box = $(this);
		$.ajax( box.data('url'), { 
			'type': 'POST',
			'async': true,
			'dataType': 'json',
			'data': {
				'pk': box.data('student-id'),
				'date': box.data('date'),
				'present': box.is(':checked') ? '1': '',
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			'beforeSend': function(xhr, settings) {
              indicator.show();
			},
			'error': function(xhr, status, error) {
                indicator.hide();
				$("#error-status").text(error).show();

				//alert(error);	
			},
			
			'success': function(data, status, xhr) {
				indicator.hide();
			}
		});
	});
}

$(document).ready(function(){
  initJournal();
  initGroupSelector();
  initDateFields();

  $('.input-group-addon').click(function() {
    initDateFields();
  });
});

//$(".input-group-addon").click( function() {
//  alert('hi');
//	//initDateFields();
//});


