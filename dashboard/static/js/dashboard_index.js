$(document).ready(function() {
	$("#club_entry").bind("go", function(e, code) {
		$("#club_entry").val(code);
		$("#entry_tracker_form").submit();
		$("#club_entry").val('');
	});	
	
	$("#entry_tracker_form").submit(function(e)
	{
	    var postData = $(this).serializeArray();
	    var formURL = $(this).attr("action");
	    $.ajax(
	    {
	        url : formURL,
	        type: "POST",
	        data : postData,
	        success:function(data, textStatus, jqXHR) 
	        {
				if (data.person_found) {					
					if (data.allowed) {
						$("<li>").html(data.first_name + " " + data.last_name).appendTo($("#club_entry_log"));
					} else {
						alert(data.first_name + " " + data.last_name + " is not allowed into the ballroom, according to current criteria");
					}
				} else {
					alert("Person not found");
				}
	        },
	        error: function(jqXHR, textStatus, errorThrown) 
	        {
	            alert("There was an error while processing the club entry. Adam has been notified.")
	        }
	    });
	    e.preventDefault(); //STOP default action
	});
});