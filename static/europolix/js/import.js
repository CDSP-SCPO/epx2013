/* javascript functions for the import application */

$(function()
{
	/* if javascript activated, hide standard upload file control and show the other one */
	$('#id_csvFile').hide();
	$('#choose_file_div').show();
});


/* display the help text (column names and order for a given file to import) */
$("#id_fileToImport").change(function()
{
	load_help_text();
});

function load_help_text()
{
	view_path=$('#help_text_view').text();
	var datastring = $('#import_form').serialize();
	$.ajax({
		type: "POST",
		url: view_path,
		dataType: 'html',
		data: datastring,
		success: function(result)
		{
			$('#help_text').html(result);
		}
	});
}

/* selection of the file */
$('#choose_file_div').click(function()
{
	choose_file($(this));
});

/* after selection of a file, remove the focus from the control (so manual paths cannot be entered) */
$("#choose_file").keypress(function()
{
	this.blur();
});


/* submit the form with ajax */
$('#import_button').click(function(event)
{
	submit_form($('#import_form'), $('#id_fileToImport'), $(this), event);
});
