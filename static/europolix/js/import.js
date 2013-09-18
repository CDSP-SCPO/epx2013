/* javascript functions for the import application */

/* display the help text (column names and order for a given file to import) */
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
			//~ alert(result.help_text);
			$('#help_text').html(result);
		}
	});
}
