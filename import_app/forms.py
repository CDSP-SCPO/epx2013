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

class CSVUploadForm(forms.Form):
    """
    FORM
    upload a csv file containing either prelex unique ids (disId) or acts to validate
    """
    file_to_import_choices=(
        ("","Select the import"),
        ('act', 'Import acts to validate'),
        ('dos_id', 'Import '+var_name_ids.var_name['dos_id']),
        ('code_agenda', 'Import '+var_name_data.var_name['code_agenda']),
        ('name', 'Import '+var_name_data.var_name['resp']+' and relative data'),
        ('dg', 'Import '+var_name_data.var_name['dg']+" and "+var_name_data.var_name['dg_sigle']),
        ('config_cons', 'Import '+var_name_data.var_name['config_cons']),
        ('adopt_pc', 'Import '+var_name_data.var_name['adopt_pc_abs']+' and '+var_name_data.var_name['adopt_pc_contre']),
        ('gvt_compo', 'Import '+var_name_data.var_name['gvt_compo']),
        ('np', 'Import opal file (NP variables)'),
        ('min_attend', 'Import Attendance of ministers'),
    )
    file_to_import=forms.ChoiceField(choices=file_to_import_choices)

    csv_file=forms.FileField(validators=[ext_validation])

    class Meta:
        model=CSVUpload
