/* act ids and info javascript functions */

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
		$('#id_actsToValidate').val('');
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
			//form valid -> displays success message
			if (mode=="save")
			{
				display_save_message(result);
				//go to the bottom of the page
				//~ alert("yes");
				$('#top_anchor').click();
			}
		});
	}
}

//display message when click on save button
function display_save_message(result)
{
	$("#msg").text(result.msg);
	//if there is already a message class on the element, remove it
	$('#msg').removeClass(function()
	{
		var match = $(this).attr('class').match(/(success|error)_msg/);
		return match ? match[0] : '';
	});
	$("#msg").addClass(result.msg_class);
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


/* display/modif or update the ids/infos of the selected act */
function display_or_update_act(button_name)
{
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

//submit the act ids or info form to save it or display validation errors
function save_act_form(form, button)
{
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


//onchange of releveAnneeModif, releveMoisModif or noOrdreModif in modif form
$("#modif_form input:text").change(function()
{
	$('#modif_button_clicked').val('no');
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
			id=element_id.slice(-1);
			$("#prelexNationResp"+id).text(result.nationResp);
			$("#prelexNationalPartyResp"+id).text(result.nationalPartyResp);
			$("#prelexEUGroupResp"+id).text(result.euGroupResp);

		}
	});
}
