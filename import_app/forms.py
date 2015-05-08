from django import forms
from django.core.exceptions import ValidationError
from models import CSVUpload
from django.conf import settings
import time
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data


def ext_validation(csv_file):
    """
    FUNCTION
    validate the extension of a file and raises an error if it is not a csv file
    PARAMETERS
    csv_file: file to upload [string]
    RETURN
    None (raise an exception if the file is not a csv file)
    """
    if not csv_file.name.endswith('.csv'):
        raise ValidationError(u'Incorrect format. Please choose a CSV file.')


def get_choices(group=""):
    """
    FUNCTION
    list of available choices for the import drop down list, in function of the user
    PARAMETERS
    group: group of the user ("" or "admin") [string]
    RETURN
    choices: list of available choices [list of tuples]
    """
    choices=[("","Select the import")]
    #imports available to the admin only
    if group=="admin":
        choices.append(('act', 'Import acts to validate'))
        choices.append(('dos_id', 'Import '+var_name_ids.var_name['dos_id']))
        choices.append(('code_agenda', 'Import '+var_name_data.var_name['code_agenda']))
        choices.append(('name', 'Import '+var_name_data.var_name['resp']+' and relative data'))
        choices.append(('dg', 'Import '+var_name_data.var_name['dg']+" and "+var_name_data.var_name['dg_sigle']))
        choices.append(('config_cons', 'Import '+var_name_data.var_name['config_cons']))
        choices.append(('adopt_pc', 'Import '+var_name_data.var_name['adopt_pc_abs']+' and '+var_name_data.var_name['adopt_pc_contre']))
        choices.append(('gvt_compo', 'Import '+var_name_data.var_name['gvt_compo']))
        choices.append(('np', 'Import opal file (NP variables)'))
        choices.append(('min_attend_insert', 'Import new Attendance of ministers'))
        choices.append(('rapp_party_family', 'Import party families of Rapporteurs'))
        choices.append(('group_votes', 'Import '+var_name_data.var_name['group_votes']))

    #import available to everyone (except temporary persons)
    choices.append(('min_attend_update', 'Update Attendance of ministers'))

    return choices


class CSVUploadForm(forms.Form):
    """
    FORM
    upload a csv file containing data to import
    """
    file_to_import=forms.ChoiceField(choices=get_choices())

    csv_file=forms.FileField(validators=[ext_validation])

    class Meta:
        model=CSVUpload

    def __init__(self, user, *args, **kwargs):
        #show all the different imports to the administrator only
        self.user = user
        super(CSVUploadForm, self).__init__(*args, **kwargs)
        if self.user.is_superuser:
            self.fields['file_to_import'].choices = get_choices("admin")
