/* modal javascript functions */
/* used for: add a dg, add a resp */

/* save add modal */
$('#modal_add').on('click', '#modal_button', function(event)
{
    modal_save_form($("#form_add"), $(this), event);
});

//show django errors
function modal_display_errors(errors)
{
    for (var key in errors)
    {
        if (key=="__all__")
        {
            $field=$("#id_"+key+"errors");
        }
        else
        {
            $field=$("#id_"+key+"_errors");
        }
        $field.html('<ul class="errorlist"><li>'+errors[key]+'</li></ul>');
    }
}

//display message when click on save button
function modal_display_message(result)
{
    //if there is already a message class on the element, remove it
    $('#form_add_msg').removeClass(function()
    {
        var match=$(this).attr('class').match(/(success|error)_msg/);
        return match ? match[0] : '';
    });
    $("#form_add_msg").addClass(result.msg_class);
    $("#form_add_msg").text(result.msg);
}

//submit the add dg / responsible form to save it or display validation errors
function modal_save_form(form, button, event)
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
                //append current errors to the html form
                modal_display_errors(result.form_errors);
                //display success or error message
                modal_display_message(result);

                if(result.hasOwnProperty('new_id'))
                {
                    new_id=result.new_id
                    new_value=result.new_value
                    drop_down_list_id=$("#var_id").html()+"_id"
                    var defaultSelected = false;
                    var nowSelected     = true;
                    //update drop down list if add was successful
                    $('#'+drop_down_list_id).append( new Option(new_value,new_id,defaultSelected,nowSelected) );

                    //update related fields
                    if ($("#var").html()=="dg")
                    {
                        update_dg(drop_down_list_id, new_id)
                    }
                    else if ($("#var").html()=="resp")
                    {
                        update_person(drop_down_list_id, new_id, "resp")
                    }
                }

            }
            //stops the loading state of the button
            button.button('reset');
        }
    });

    //don't submit the form
    return false;
}
