/* jquery functions for the login application */

/* submit form if press enter on the last control */
$("#password").keypress(function(event)
{
	if (event.keyCode == 13)
	{
		$('#login_button').click();
		event.preventDefault();
	}
});

/* submit the form with ajax */
$('#login_button').click(function(event)
{
	submit_form($('#login_form'), 'no', $(this), event);
});
