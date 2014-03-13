/* jquery functions for the europolix project */


//change the active link in the menu on startup
$('#menu a[href*="' + location.pathname.split("/")[2] + '"][class!="noselect"]').parent().addClass('active');


//show loading page data or error message
function show_msg(msg, msg_class)
{
    $("#loading")
        .html(msg)
        .removeClass()
        .addClass(msg_class)
    $("#loading_div").show();
}

//hide loading page data or error message
function hide_msg()
{
    $("#loading_div").hide();
}


//select a file to upload
function choose_file($div)
{
    hidden_input_file=$div.prev();
    visible_input_file=$div.find('input');
    $(hidden_input_file).click();

    $(hidden_input_file).change(function()
    {
        var index=$(this).val().lastIndexOf("\\") + 1;
        var file_name=$(this).val().substr(index);
        $(visible_input_file).val(file_name);
    });

    $(visible_input_file).blur();
    $div.blur();
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
    $("#errors").empty();
}

//reset a form (input text, textarea and checkbox)
function reset_form($form)
{
    $form.find('input:text, textarea').val('');
    $form.find('input:checkbox').removeAttr('checked').removeAttr('selected');
}


//handle django view return
function handle_result(form, result)
{
    //reload menu if click on login button and success
    if (form.attr("id")=="login_form" && result.msg_class=="success_msg")
    {
        //~ alert(result.user.username);
        reload_menu(result.user.username);
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
            var match=$(this).attr('class').match(/(success|error)_msg/);
            return match ? match[0] : '';
        });
        $("#msg").addClass(result.msg_class);

        //display errors (import)
        if (form.attr("id")=="import_form")
        {
            errors="";
            for ( var i=0; i < result.errors.length; i++ )
            {
                errors+='<div class="row-fluid error_msg">'+result.errors[i]+'</div>';
            }
            $("#errors").html(errors);
        }

        //reset the form
        //~ reset_form(form);
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
        show_msg("Something is not right. Please reload the page and try again.", "alert alert-error");
        //hide the message after a few seconds
        window.setTimeout(hide_msg, 10000);
        window.console&&console.log(xhr.responseText);
        //for administrator only (or deactivate the javascript)
        //alert("An AJAX error occured: " + status + "\n" + error);
        alert("An error occured. Please reload the page and try again. If the problem persists, please contact the administrator.");
    }
});

//from a menu link, load the content of the page (right side) with Ajax (no need to reload the menu and header)
$('.internal_link').click(function(event)
{
    load_content($(this), event);
});


/* reload the left menu when a user log in or log out */
function reload_menu(username)
{
    //~ alert("username"+username+"\n"+"path"+$("#reload_menu_view").text())


    $("#sidebar_and_content").load($("#reload_menu_view").text(), {"username": username}, function()
    {
        //~ alert("ok");
    });

}


function load_content($a, event)
{
    //do not follow the href link
    event.preventDefault();

    //get link
    link=$a.attr("href")

    //show message ("the page is being loaded")
    show_msg("The page is being loaded...", "alert alert-data");

    //logout
    if (link.match(/login/))
    {
        reload_menu("")
    }

    $.get(link, function(data)
    {
        var title=$(data).find("#title");
        var content=$(data).find("#content");
        $("#title_base").html(title);
        $("#content_base").html(content);

        //hide message ("the page is being loaded")
        hide_msg();
    });

    //change the active link in the menu
    $('.active').removeClass('active');
    $a.parent().addClass('active');
}

//create an iframe in the current form
function iframe_creation()
{
    var iframe=$('<iframe name="postiframe" id="postiframe" style="display: none" />');
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
    //if import form
    if (file!="")
    {
        form.attr("enctype", "multipart/form-data");
        form.attr("encoding", "multipart/form-data");
        form.attr("file", $(file).val());
    }
    form.attr("target", $(iframe).attr("id"));
    /* tells the view the result must be loaded in an iframe -> json */
    var input=$("<input>").attr("type", "hidden").attr("name", "iframe");
    form.append($(input));
    form.submit();
}


/* submit a form containing a file to upload or download */
function send_file(form, link, file, callback)
{
    //create iframe
    var iframe=iframe_creation();

    //submit data to iframe
    post_iframe(iframe, form, link, file)

    //export form: if no error, no iframe load
    if (form.attr("id")=="export_form" && $("#id_sort_fields").val()!="" && $("#id_sort_direction").val()!="")
    {
        acts_nb=$("#acts_nb").val();
        var result={
        "msg": acts_nb+" act(s) are being downloaded...",
        "msg_class": "success_msg"
        };

        callback(JSON.stringify(result));
    }

    //import form
    $(iframe).load(function ()
    {
        //get result sent by the view and loaded into the iframe
        var body=window.frames[$(iframe).attr("name")].document.body;
        result=(body.textContent || body.innerText);
        callback(result);
    });

}


//submit a form and display an error or succes message with Ajax
function submit_form($form, file, button, event)
{
    //do not reload the page
    event.preventDefault();

    //post link
    link=$form.attr("action");

    //loading state for the button (use bootstrap function)
    button.button('loading');
    //remove previous errors (from the previous run)
    remove_previous_errors();

    //download or upload a file (export or import form)
    if (file!="no")
    {
        //function(result)-> wait till the load is over and return the result variable (content of iframe)
        result=send_file($form, link, file, function(result)
        {
            handle_result($form, $.parseJSON(result));
            //stops the loading state of the button
            button.button('reset');
        });
    }
    else
    {
        //otherwise ajax to post the data
        var form_data=$form.serialize();
        $.ajax
        ({
            type: 'POST',
            url: link,
            dataType: 'json',
            data: form_data,
            success: function(result)
            {
                //display success or error message
                handle_result($form, result);
                //stops the loading state of the button
                $(button).button('reset');
            }
        });
    }
}
