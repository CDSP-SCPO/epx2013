/* javascript functions for the attendance application */

alert("ok");

//reset attendance form
function reset_attendance_form(result, mode)
{
    if (mode=="display")
    {
        //display act
        $('#attendance_form_div').html(result);
    }
    else
    {
        //reset form
        $('#attendance_form_div').load($("#reset_form_path").text(), function()
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
}


//show django errors
function display_errors(errors, form_index)
{
    //~ for field in errors
    //~ alert("hello")
    //~ alert(errors)
    //~ var errors = JSON.parse(errors);
    //~ for (i=0;i<errors.length;i++)
    //~ {
        //~ alert(errors[i])
    //~ }

    /* key=field name, example: form-0-country */
    for (var key in errors)
    {
        if (key=="__all__")
        {
            /* id_form-0_errors */
            $field=$("#id_form-"+form_index+"_errors");
        }
        else
        {
            /* id_form-0-country_errors */
            $field=$("#id_"+key+"_errors");
        }
        $field.html('<ul class="errorlist"><li>'+errors[key]+'</li></ul>');
    }
}


/* handle django view return when displaying an act from the drop down list (add form) or mdifying an act (modif form)
action = "add_attendance" or "modif_attendance" or "update_status" */
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
        //reset act form except if click on update status button
        if(!result.update_status_errors)
        {
            //reset attendance form
            reset_attendance_form(result, "reset");
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
        //display act in attendance form
        if(!result.modif_act_errors)
        {
            reset_attendance_form(result, "display");
        }
    }
}


//handle django view return when saving an act
function save_result(result)
{
    //form not valid -> displays errors
    if (result.save_attendance_errors)
    {
        if (result.mode=="add")
        {
            //reset modif form
            reset_modif("all");
        }

        //append current errors to the html form
        errors=result.save_attendance_errors;
        display_errors(errors, "update_status");
        display_save_message(result);
    }
    else
    {
        //act saved, reset everything

        //display act in attendance form
        reset_attendance_form(result, "save");
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
    display_or_update_attendance("add_act", event);
});


/* update of status */
$('#attendance_form').on('click', '#update_status', function(event)
{
    if ($(this).attr('name')=="modif_act")
    {
        //tells the view we are trying to modif an act
        $('#modif_button_clicked').val('yes');
    }
    display_or_update_attendance($(this).attr('name'), event);
});

/* display/modif or update the selected act */
function display_or_update_attendance(button_name, event)
{
    //do not follow the href link
    event.preventDefault();

    //show loading gif
    $("#loading_gif_"+button_name).show();

    form=$('#attendance_form');
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
$('#attendance_form').on('click', '#save_attendance', function(event)
{
    alert("youpi");
    save_attendance_form($("#attendance_form"), $(this), event);
});


//submit the attendace form to save it or display validation errors
function save_attendance_form(form, button, event)
{
    alert("ok");
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
        },
        error: function(error)
        {
            alert( "error" );
        }
    });

    //don't submit the form
    return false;
}
