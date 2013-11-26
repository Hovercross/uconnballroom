$(document).ready(function() {
	$("#person_info_search").bind("go", function(e, code) {
		$("#person_info_search").val(code);
		$("#person_info_form").submit();
	});	
});