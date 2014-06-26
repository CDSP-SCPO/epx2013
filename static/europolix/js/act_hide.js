/* elements to show / hide when javascript is activated on act ids and act data forms */

/* if javascript activated, hide add act button (act ids) */
$('#add_act').hide();
/* if javascript activated, hide all the update buttons (act data) */
$('.update_btn').hide();
/* add dg link */
$('.add_dg_no_js').hide();
$('.add_dg_js').show();
/* add rapp link */
$('.add_rapp_no_js').hide();
$('.add_rapp_js').show();
/* add resp link */
$('.add_resp_no_js').hide();
$('.add_resp_js').show();

/* hide drop down lists for adopt fields */
$.each(["adopt_cs_contre_", "adopt_pc_contre_", "adopt_cs_abs_", "adopt_pc_abs_"], function( index, name ) 
{
    for (var n = 1; n < 9; n++)
    {
         $('#id_'+name+n).hide();
    }
});
