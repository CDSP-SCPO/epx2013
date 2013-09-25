/* act ids and info javascript functions */
$(function()
{
	/* if javascript activated, hide add act button (act ids) */
	$('#add_div  #add_act').hide();
	/* if javascript activated, hide respPropos update act button (act info) */
	$('#prelex_table .update_respPropos').hide();

});

/* submit form if press enter on the last control */
$("#id_noOrdreModif").keypress(function(event)
{
	if (event.keyCode == 13)
	{
		$('#modif_act').click();
		event.preventDefault();
	}
});


//onchange of releveAnneeModif, releveMoisModif or noOrdreModif in modif form
$("#modif_form input:text").change(function()
{
	$('#modif_button_clicked').val('no');
});


//reset add form
function reset_add_form(what, saved)
{
	//an act has been validated
	if (saved=="yes")
	{
		//reset drop down list
		$("#id_actsToValidate option:selected").remove();
		//number of acts to validate
		nb=$("#acts_nb").text().match(/(\d+)/g);
		$("#acts_nb").text(parseInt(nb)-1+" act(s) to validate!");
	}

	if (what=="all")
	{
		//select empty and default value
		$('#id_actsToValidate').val('');
		//~ $("#id_actsToValidate option[value='']").attr('selected', true)
	}

	$('#add_div .errorlist').each(function()
	{
		$(this).remove();
	});
}

//reset modif form
function reset_modif_form(what)
{
	//reset fields
	if (what=="all")
	{
		$("#modif_div input:text").val('');
	}
	//reset errors
	$('#modif_div .errorlist').each(function()
	{
		$(this).remove();
	});

	//reset heights of errors
	$('#add_modif .modif_errors').height("auto");
}

//reset act form
function reset_act_form(result, mode)
{
	if (mode=="display")
	{
		//display act
		$('#act_form_div').html(result);
	}
	else
	{
		//reset form
		$('#act_form_div').load($("#reset_form_path").text(), function()
		{
			//on save: form valid -> displays success message
			if (mode=="save")
			{
				display_save_message(result);
				//go to the bottom of the page
				$('#top_anchor').click();
			}
		});
	}

	/* if javascript activated, hide respPropos update act button (act info) */
	$('#prelex_table .update_respPropos').hide();
}

//display message when click on save button
function display_save_message(result)
{
	//if there is already a message class on the element, remove it
	$('#msg').removeClass(function()
	{
		var match = $(this).attr('class').match(/(success|error)_msg/);
		return match ? match[0] : '';
	});
	$("#msg").addClass(result.msg_class);
	$("#msg").text(result.msg);
}

//show django errors
function display_errors(errors, action)
{
	for (var key in errors)
	{
		if (key=="__all__")
		{
			$field=$("#id_"+action+key+"errors");
		}
		else
		{
			$field=$("#id_"+key+"_errors");
		}
		$field.html('<ul class="errorlist"><li>'+errors[key]+'</li></ul>');
	}
}

//handle django view return (act ids and act info) when displaying an act from the drop down list (add form) or mdifying an act (modif form)
function display_or_update_result(result, action)
{
	//add mode -> an act has been selected in the drop down list
	if (action=="add_act")
	{
		//reset add and modif form
		reset_add_form("errors", "no");
		reset_modif_form("all");
	}
	else if(action=="modif_act")
	{
		//reset add and modif form
		reset_add_form("all", "no");
		reset_modif_form("errors");
	}

	//validation errors
	if(result.hasOwnProperty(action+'_errors'))
	{
		//reset act form except if click on update button
		if(!result.update_act_errors)
		{
			//reset act form
			reset_act_form(result, "reset");
		}

		//append current errors to the html form
		errors=eval(result[action+"_errors"]);
		display_errors(errors, action);

		//ajust height divs for the modif_form
		if (action=="modif_act")
		{
			var maxHeight = Math.max.apply(null, $('#add_modif .modif_errors').map(function ()
			{
				return $(this).height();
			}).get());

			$('#add_modif .modif_errors').height(maxHeight);
		}
	}
	else
	{
		//display act in act form
		reset_act_form(result, "display");
	}
}


//handle django view return (act ids and act info) when saving an act
function save_result(result)
{
	//form not valid -> displays errors
	if (result.save_act_errors)
	{
		if (result.mode=="add")
		{
			//reset modif form
			reset_modif_form("all");
		}

		//append current errors to the html form
		errors=result.save_act_errors;
		display_errors(errors, "update_act");
		display_save_message(result);
	}
	else
	{
		//display act in act form
		reset_act_form(result, "save");
		//reset add and modif form
		if (result.mode=="add")
		{
			reset_add_form("all", "yes");
		}
		else
		{
			reset_add_form("all", "no");
		}
		reset_modif_form("all");
	}
}

/* add of an act (selection from drop down list) */
$("#add_div select").change(function(event)
{
	display_or_update_act("add_act", event);
});


/* modification or update an act (act ids form) */
$('body').on('click', '#modif_act, #update_act', function(event)
{
	if ($(this).attr('name')=="modif_act")
	{
		//tells the view we are trying to modif an act
		$('#modif_button_clicked').val('yes');
	}
	display_or_update_act($(this).attr('name'), event);
});

/* display/modif or update the ids/infos of the selected act */
function display_or_update_act(button_name, event)
{
	//do not follow the href link
	event.preventDefault();

	//show loading gif
	$("#loading_gif_"+button_name).show();

	form=$('#act_form');
	var form_data = form.serialize();
	form_data+="&"+button_name+"=''";

	$.ajax
	({
		type: "POST",
		url: form.attr('action'),
		//~ dataType: 'html',
		data: form_data,
		success: function(result)
		{
			//if an act has been selected, either from the add form or the modif form
			if (result!="")
			{
				//display or mpdify an act
				display_or_update_result(result, button_name);
			}
			//hide loading gif
			$("#loading_gif_"+button_name).hide();
		}
	});

	//don't submit the form
	return false;
}


/* save an act*/
$('#act_form').on('click', '#save_act', function(event)
{
	save_act_form($("#act_form"), $(this), event);
});


//submit the act ids or info form to save it or display validation errors
function save_act_form(form, button, event)
{
	//do not follow the href link
	event.preventDefault();

	//loading state for the button (use bootstrap function)
	button.button('loading');
	//remove previous errors (from the previous run) -> modif form
	$('.errorlist').each(function()
	{
		$(this).remove();
	});
	var form_data = form.serialize();
	form_data+="&"+button.attr("id")+"=''";
	$.ajax
	({
		type: 'POST',
		url: form.attr('action'),
		dataType: 'json',
		data: form_data,
		success: function(result)
		{
			//if an act has been selected, either from the add form or the modif form
			if (result!="")
			{
				//display success or error message
				save_result(result);
			}
			//stops the loading state of the button
			button.button('reset');
		}
	});

	//don't submit the form
	return false;
}


/* update a respPropos */
$('body').on('change', '#prelexRespProposId1_id, #prelexRespProposId2_id, #prelexRespProposId3_id', function()
{
	update_respPropos(this.id, this.value);
});


/* update the respPropos variables when a different respPropos is selected from the drop down list */
function update_respPropos(element_id, respPropos_id)
{
	$.ajax
	({
		type: 'POST',
		url: $("#respPropos").text(),
		dataType: 'json',
		data: "respPropos_id="+respPropos_id,
		success: function(result)
		{
			//get the number of respPropos 1, 2 or 3
			id=element_id.slice(-4, -3);
			$("#prelexNationResp"+id).text(result.nationResp);
			$("#prelexNationalPartyResp"+id).text(result.nationalPartyResp);
			$("#prelexEUGroupResp"+id).text(result.euGroupResp);

		}
	});
}
