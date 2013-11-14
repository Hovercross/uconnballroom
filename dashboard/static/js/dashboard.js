$( document ).ready(setupAutocomplete);

directSearch = /^((pe[0-9]{1,})|(rf[0-9]{1,})|(mc[0-9]{2}(f|s)[0-9]{1,})|(rl[0-9]{1,})|(pc[0-9]{1,}))$/i;

function setupAutocomplete() {
	autocomplete = $(".autocomplete").autocomplete({
		source: '/dashboard/autocomplete/',
		minlength: 2,
		delay: 500,
		select: function(event,ui) {
			$(this).trigger("go", "PE" + ui.item.id);
		},
		response: function(event, ui) {
			$(this).data("responses", ui.content);
		}
	});
	
	autocomplete.data( "ui-autocomplete" )._renderItem = function( ul, item ) {
		emails = item.emails;
		name = (item.first_name + " " + item.last_name).trim();
		
		li = $( "<li>" ).appendTo(ul);
		li.data( "ui-autocomplete-item", item );
		a = $("<a>").appendTo(li);

		if (name) {
			$("<span>").html(item.first_name + " " + item.last_name).addClass("autocomplete-name").appendTo(a);
		} else {
			$("<span>").html("Name unknown").addClass("autocomplete-name-empty").appendTo(a);
		}
		
		
		if(emails) {
			$("<br>").appendTo(a);
			$("<span>").html(emails.join(", ")).addClass("autocomplete-emails").appendTo(a);
		}
		
		
		return li;
	};
	
	autocomplete.keyup(function(e){
	    if(e.keyCode == 13)
	    {
			value = $(this).val();
			if (directSearch.test(value)) {
				$(this).trigger("go", value);
			} else {
				results = $(this).data("responses");
				$(this).data("responses", false);
				if(results) {
					$(this).trigger("go", "PE" + results[0].id);
					$(this).autocomplete("close");
				}
			}
	    } 
	});
}