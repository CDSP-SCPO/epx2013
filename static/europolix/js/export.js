/* javascript functions for the export application */


/* submit the form with ajax */
$('#export_button').click(function(event)
{
	submit_form($('#export_form'), '', $(this), event);
});
