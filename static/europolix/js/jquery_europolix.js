/* jquery functions for the europolix project */


//change the active link in the menu on startup
$('#menu a[href*="' + location.pathname.split("/")[2] + '"][class!="noselect"]').parent().addClass('active');


//show loading page info or error message
function show_msg(msg, msg_class)
{
	$("#loading")
		.html(msg)
		.removeClass()
		.addClass(msg_class)
	$("#loading_div").show();
}

//hide loading page info or error message
function hide_msg()
{
	$("#loading_div").hide();
}


//select a file to upload
function choose_file(div)
{
	hidden_input_file=$(div).prev();
	visible_input_file=$(div).find('input');
	$(hidden_input_file).click();

	$(hidden_input_file).change(function()
	{
		var index = $(this).val().lastIndexOf("\\") + 1;
		var filename = $(this).val().substr(index);
		$(visible_input_file).val(filename);
	});

	$(visible_input_file).blur();
	$(div).blur();
}


//remove previous errors (from the previous run)
function remove_previous_errors()
{
	$("#msg").empty();
	$('.errorlist').each(function()
	{
		$(this).remove();
	});
	//import form
	$("#errors_list").empty();
}

//reset a form (input text, textarea and checkbox)
function resetForm($form)
{
	$form.find('input:text, textarea').val('');
	$form.find('input:checkbox').removeAttr('checked').removeAttr('selected');
}


//handle django view return
function handle_result(form, result)
{
	//change the welcome message (login form)
	if (form.attr("id")=="login_form")
	{
		username=(result.username)? result.username: "visitor";
		$("#welcome_user").text("Welcome "+username+"!");
	}

	//form not valid -> displays errors
	if (result.form_errors)
	{
		//append current errors to the html form
		errors=result.form_errors
		for (var key in errors)
		{
			$("#id_"+key+"_errors").html('<ul class="errorlist"><li>'+errors[key]+'</li></ul>');
		}
	}
	else
	{
		//form valid -> displays message
		$("#msg").text(result.msg);
		//if there is already a message class on the element, remove it
		$('#msg').removeClass(function()
		{
			var match = $(this).attr('class').match(/(success|error)_msg/);
			return match ? match[0] : '';
		});
		$("#msg").addClass(result.msg_class);

		//display errors_list (import)
		if (form.attr("id")=="import_form")
		{
			errors_list="";
			for ( var i = 0; i < result.errors_list.length; i++ )
			{
				errors_list+='<div class="row-fluid error_msg">'+result.errors_list[i]+'</div>';
			}
			$("#errors_list").html(errors_list);
		}

		//reset the form
		//~ resetForm(form);
	}
}




//AJAX

//display ajax errors
$.ajaxSetup
({
	error: function(xhr, status, error)
	{
		//show error message
		window.scrollTo(0, 0);
		show_msg("Something is not right. Please try again.", "alert alert-error");
		//hide the message after a few seconds
		window.setTimeout(hide_msg, 7000);
		window.console&&console.log(xhr.responseText);
		alert("An AJAX error occured: " + status + "\nError: " + error);
	}
});

//load the content of the page (right side) with Ajax (no need to reload the menu and header)
function load_content(a, link)
{
	//show message ("the page is being loaded")
	show_msg("The page is being loaded...", "alert alert-info");

	//change the welcome message (login form)
	if (link.match(/login/))
	{
		$("#welcome_user").text("Welcome visitor!");
	}

	$.get(link, function(data)
	{
		//~ alert(data)
		var title=$(data).find("#title");
		var content=$(data).find("#content");
		$("#title_base").html(title);
		$("#content_base").html(content);

		//hide message ("the page is being loaded")
		hide_msg();
	});

	//change the active link in the menu
	$('.active').removeClass('active');
	$(a).parent().addClass('active');
}

//create an iframe in the current form
function iframe_creation()
{
	var iframe = $('<iframe name="postiframe" id="postiframe" style="display: none" />');
	//remove the previous iframe if more than one click on the submit button
	$("#"+$(iframe).attr("id")).remove();
	//append the iframe to the html page
	$("body").append(iframe);
	return iframe;
}

//post a form via an iframe
function post_iframe(iframe, form, link, file)
{
	form.attr("action", link);
	form.attr("method", "post");
	if (file!="")
	{
		form.attr("enctype", "multipart/form-data");
		form.attr("encoding", "multipart/form-data");
		form.attr("file", $(file).val());
	}
	form.attr("target", $(iframe).attr("id"));
	form.submit();
}


/* submit a form containing a file to upload or download */
function send_file(form, link, file, loadCallback)
{
	//create iframe
	var iframe=iframe_creation();

	//submit data to iframe
	post_iframe(iframe, form, link, file)

	//export form: if no error, no iframe load
	if (form.attr("id")=="export" && $("#id_sortFields").val()!="" && $("#id_sortDirection").val()!="")
	{
		var result = {
		"msg": "The acts are being downloaded...",
		"msg_class": "success_msg"
		};

		loadCallback(JSON.stringify(result));
	}

	//import form
	$(iframe).load(function ()
	{
		//get result sent by the view and loaded into the iframe
		var body=window.frames[$(iframe).attr("name")].document.body;
		result=(body.textContent || body.innerText);
		loadCallback(result);
	});

}


var myTrigger;


//submit a form and display an error or succes message with Ajax
function submit_form(form, link, file, button)
{
	//loading state for the button (use bootstrap function)
	button.button('loading');
	//remove previous errors (from the previous run)
	remove_previous_errors();

	//download or upload a file (export or import form)
	if (file!="no")
	{
		//function(result)-> wait till the load is over and return the result variable (content of iframe)
		result=send_file(form, link, file, function(result)
		{
			handle_result(form, $.parseJSON(result));
			//stops the loading state of the button
			button.button('reset');
		});
	}
	else
	{
		//otherwise ajax to post the data
		var form_data = form.serialize();
		$.ajax
		({
			type: 'POST',
			url: link,
			dataType: 'json',
			data: form_data,
			beforeSend: function (thisXHR)
			{
				myTrigger = setInterval (function ()
				{
					if (thisXHR.readyState > 2)
					{
						var totalBytes  = thisXHR.getResponseHeader('Content-length');
						var dlBytes=thisXHR.responseText.length;
						(totalBytes > 0)? alert(Math.round((dlBytes/ totalBytes) * 100) +"%"): alert(Math.round (dlBytes / 1024) + "K");
					}
				}, 200);
			},
			complete: function ()
			{
				clearInterval (myTrigger);
			},
			success: function(result)
			{
				//display success or error message
				handle_result(form, result);
				//stops the loading state of the button
				$(button).button('reset');
			}
		});
	}

	//don't submit the form
	return false;
}
