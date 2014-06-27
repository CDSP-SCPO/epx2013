/* javascript function for the add/modif form */

/* submit form if press enter on the last control */
$("#id_no_ordre_modif").keypress(function(event)
{
    if (event.keyCode==13)
    {
        $('#modif_act').click();
        event.preventDefault();
    }
});

$("#id_releve_annee_modif").keypress(function() 
{
    if($(this).val().length == 3) 
    {
       $("#id_releve_mois_modif").focus();  
    }
});

$("#id_releve_mois_modif").keypress(function() 
{
    if($(this).val().length == 1) 
    {
       $("#id_no_ordre_modif").focus();  
    }
});

$("#id_releve_mois_modif").keyup(function() 
{
    if($(this).val().length == 1 && $(this).val()>1)
    {
       $("#id_no_ordre_modif").focus();  
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
