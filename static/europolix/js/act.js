/* act ids and data javascript functions */

/* submit form if press enter on the last control */
$("#id_no_ordre_modif").keypress(function(event)
{
	if (event.keyCode==13)
	{
		$('#modif_act').click();
		event.preventDefault();
	}
});


//onchange of releve_annee_modif, releve_mois_modif or no_ordre_modif in modif form
$("#id_releve_annee_modif, #id_releve_mois_modif, #id_no_ordre_modif").change(function()
{
	$('#modif_button_clicked').val('no');
});


//reset add form
function reset_add(what, saved)
{
	//an act has been validated
	if (saved=="yes")
	{
		//reset drop down list
		$("#id_act_to_validate option:selected").remove();
		//number of acts to validate
		nb=$("#acts_nb").text().match(/(\d+)/g);
		$("#acts_nb").text(parseInt(nb)-1+" act(s) to validate!");
	}

	if (what=="all")
	{
		//select empty and default value
		$('#id_act_to_validate').val('');
		//~ $("#id_act_to_validate option[value='']").attr('selected', true)
	}

	$('#add_div .errorlist').each(function()
	{
		$(this).remove();
	});
}

//reset modif form
function reset_modif(what)
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

	//~ //reset heights of errors
	$('#add_modif .modif_errors').height("auto");
}

//reset act form
function reset_act_form(result, mode)
{
	if (mode=="display")
	{
		//display act
		$('#act_form_div').html(result);

		/* if javascript activated, hide person update button (act data) */
		$('.update_person').hide();
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

				/* if javascript activated, hide person update button (act data) */
				$('.update_person').hide();
			}
		});
	}
}

//display message when click on save button
function display_save_message(result)
{
	alert('youpi');
	//if there is already a message class on the element, remove it
	$('#msg').removeClass(function()
	{
		var match=$(this).attr('class').match(/(success|error)_msg/);
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

//handle django view return (act ids and act data) when displaying an act from the drop down list (add form) or mdifying an act (modif form)
function display_or_update_result(result, action)
{
	//add mode -> an act has been selected in the drop down list
	if (action=="add_act")
	{
		//reset add and modif form
		reset_add("errors", "no");
		reset_modif("all");
	}
	else if(action=="modif_act")
	{
		//reset add and modif form
		reset_add("all", "no");
		reset_modif("errors");
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

		//ajust height divs for the modif
		if (action=="modif_act")
		{
			var maxHeight=Math.max.apply(null, $('.modif_errors').map(function ()
			{
				return $(this).height();
			}).get());

			$('.modif_errors').height(maxHeight);
		}
	}
	else
	{
		//display act in act form
		if(!result.modif_act_errors)
		{
			reset_act_form(result, "display");
		}
	}
}


//handle django view return (act ids and act data) when saving an act
function save_result(result)
{
	//form not valid -> displays errors
	if (result.save_act_errors)
	{
		if (result.mode=="add")
		{
			//reset modif form
			reset_modif("all");
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
			reset_add("all", "yes");
		}
		else
		{
			reset_add("all", "no");
		}
		reset_modif("all");
	}
}

/* add of an act (selection from drop down list) */
$("#id_act_to_validate").change(function(event)
{
	display_or_update_act("add_act", event);
});


/* modification or update of an act (act ids form) */
$('#act_form').on('click', '#modif_act, #update_act', function(event)
{
	if ($(this).attr('name')=="modif_act")
	{
		//tells the view we are trying to modif an act
		$('#modif_button_clicked').val('yes');
	}
	display_or_update_act($(this).attr('name'), event);
});

/* display/modif or update the ids/datas of the selected act */
function display_or_update_act(button_name, event)
{
	//do not follow the href link
	event.preventDefault();

	//show loading gif
	$("#loading_gif_"+button_name).show();

	form=$('#act_form');
	var form_data=form.serialize();
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


//submit the act ids or data form to save it or display validation errors
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
	var form_data=form.serialize();
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


/* bind the event to update code_sects with the associated drop down list */
$('#act_form').on('change', '#code_sect_1_id, #code_sect_2_id, #code_sect_3_id, #code_sect_4_id', function()
{
	update_code_sect(this.id, this.value);
});

/* bind the event to update rapps with the associated drop down list */
$('#act_form').on('change', '#rapp_1_id, #rapp_2_id, #rapp_3_id, #rapp_4_id, #rapp_5_id', function()
{
	update_person(this.id, this.value, "rapp");
});

/* bind the event to update a dg with the associated drop down list */
$('#act_form').on('change', '#dg_1_id, #dg_2_id', function()
{
	update_dg(this.id, this.value);
});

/* bind the event to update resps with the associated drop down list */
$('#act_form').on('change', '#resp_1_id, #resp_2_id, #resp_3_id', function()
{
	update_person(this.id, this.value, "resp");
});


/* update the code_agenda when a different code_sect is selected from the drop down list */
function update_code_sect(name, value)
{
	$.ajax
	({
		type: 'POST',
		url: $("#code_sect").text(),
		dataType: 'json',
		data: "code_sect_id="+value,
		success: function(result)
		{
			//get the number of code_sect (code_sect_1_id, code_sect_2_id, code_sect_3_id, code_sect_4_id)
			id=name.slice(-4,-3);
			$("#code_agenda_"+id).text(result.code_agenda);
		}
	});
}

/* update the code_sect variables when a different code_sect is selected from the drop down list */
function update_person(name, value, src)
{
	$.ajax
	({
		type: 'POST',
		url: $("#person").text(),
		dataType: 'json',
		data: "person_id="+value+"&src="+src,
		success: function(result)
		{
			//get the number of person (1, 2, 3)
			id=name.slice(-4,-3);
			$("#"+src+"_country_"+id).text(result.country);
			$("#"+src+"_party_"+id).text(result.party);
			if (src=="resp")
			{
				/* party_family only for resps */
				$("#"+src+"_party_family_"+id).text(result.party_family);
			}
		}
	});
}

/* update the dg_sigle when a different dg is selected from the drop down list */
function update_dg(name, value)
{
	$.ajax
	({
		type: 'POST',
		url: $("#dg").text(),
		dataType: 'json',
		data: "dg_id="+value,
		success: function(result)
		{
			//get the number of dg (dg_1_id, dg_2_id)
			id=name.slice(-4,-3);
			$("#dg_sigle_"+id).text(result.dg_sigle);
		}
	});
}


/* modal add dg / resp*/

/* bind the event to update a dg /resp with the associated drop down list */
$('#act_form').on('click', '.add_dg_js, .add_resp_js', function()
{
	//fill the hidden div with the name of the drop down list to update (if add a record with the modal)
	field_id=this.id;
	field_id=field_id.substr(field_id.indexOf("_") + 1);
	$("#modal_field").html(field_id);

	variables = $(this).data('id').split(";");
	field=variables[0]
	name=variables[1]
	url="/db_mgmt/form_add.html/"+field+"/"

	$.get(url, function(data)
	{
		$('#modal_add')
		.find('#modal_title').html("Add a new "+name)
		.end()
		.find('#modal_content').html($(data))
		.end()
		.find('#div_button_add').hide()
		.end()
		.find("#var_id").html(field_id)
	});
});
