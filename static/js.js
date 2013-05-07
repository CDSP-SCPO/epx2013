/* 
 * actsValidation form 
 * displays the fields corresponding to the source selection
 */
 
function actToValidateDisplay(actDic)
{

	//~ jsontext = lawDic.replace("'", "\"");
	//~ alert(jsontext)
    //~ var jsonData = eval('(' + jsontext+ ')');
    //~ alert(jsonData)
    
	//~ newLawDic = lawDic.replace(/L/g, "");
	//~ var obj = jQuery.parseJSON('{"name":"John"}')
	//~ var newLawDic = jQuery.parseJSON(newLawDic)
	//~ 
	//~ mystring=str(lawDic)
	//~ alert(newLawDic)
	alert(actDic);
	/*
	 * on change of source choice 
	 * displays corresponding fields, retrieved data form and reset form if the previous law has been saved
	 */
	 
	/*reset form*/
	//~ if  ($('#idsForm').is(":visible"))
	//~ {
//~ 
	//~ }
	//~ 
	//~ choicesValue=$('#id_source').val();
	//~ $("#prelexWithDosId").hide();
	//~ $('#idsForm').show();


	
}

//~ 
//~ $(function()
//~ { 
	//~ $('#id_source').change(makeIdsVisible);
//~ });

$(document).ready(function() {
	/* 
	 * lawsValidation form 
	 * onchange source choice -> triggers makeIdsVisible
	 */
    //~ $('#id_source').change(makeIdsVisible);
    //~ if(choicesValue=$('#id_source').val() != "")
    //~ {
		//~ $('#id_source').trigger('change') ;
	//~ }
}) ;
