/* javascript function for the add/modif form */

function grey_in_out(grey_in_div_name, grey_out_div_name)
{
    $(grey_out_div_name).css("opacity", "0.4");
    $(grey_out_div_name+" :input[type=text]").attr("disabled", true);
    
    $(grey_in_div_name).css("opacity", "1");
    $(grey_in_div_name+" :input[type=text]").attr("disabled", false);
}

/* grey out releve_ids_div or propos_ids_div */
$("input[name='ids_radio']").change(function()
{
    ids=$(this).val();
    /*click on releve ids radio button -> use releve ids to modify the act and grey out the propos ids */
    if (ids=="releve")
    {
        grey_in_out("#releve_ids_div", "#propos_ids_div");
    }
    /*click on propos ids radio button -> use propos ids to modify the act and grey out the releve ids */
    else
    {
        grey_in_out("#propos_ids_div", "#releve_ids_div");
    }
});


/* submit form if press enter on the last control */
$('#add_modif').on('keypress', '#id_no_ordre_modif, #id_propos_chrono_modif', function(event)
{
    //press enter
    if (event.keyCode==13)
    {
        $('#modif_act').click();
        event.preventDefault();
    }
});


/*if field is full, go to next field (mimic tabulation)*/

/* releve ids */
$("#id_releve_annee_modif").keypress(function() 
{
    if($(this).val().length == 3) 
    {
       $("#id_releve_mois_modif").focus();  
    }
});

/* 1, 10, 11, 12 */
$("#id_releve_mois_modif").keypress(function() 
{
    if($(this).val().length == 1) 
    {
       $("#id_no_ordre_modif").focus();  
    }
});

/* 2, 3, ..., 9 */
$("#id_releve_mois_modif").keyup(function() 
{
    if($(this).val().length == 1 && $(this).val()>1)
    {
       $("#id_no_ordre_modif").focus();  
    }
});

/* propos ids */

$("#id_propos_origine_modif").keyup(function() 
{
    array=["COM", "JAI", "BCE", "EM", "CONS", "CJEU"]
    if(jQuery.inArray($(this).val().toUpperCase(), array)!==-1)
    {
       $("#id_propos_annee_modif").focus();  
    }
});

    
$("#id_propos_annee_modif").keypress(function() 
{
    if($(this).val().length == 3) 
    {
       $("#id_propos_chrono_modif").focus();  
    }
});


//onchange of textboxes in modif form, deactivate modif mode
$("#radio_button_and_textbox_div :input").change(function()
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
    /* '#modif_div .modif_errors_releve, #modif_div .modif_errors_propos' */
    $('#modif_div .errorlist').each(function()
    {
        $(this).remove();
    });

    //~ //reset heights of errors
    $('#add_modif .modif_errors_releve, #add_modif .modif_errors_propos').height("auto");
}


/* MAIN  */

/* grey out propos ids and grey in releve ids */
grey_in_out("#releve_ids_div", "#propos_ids_div");
