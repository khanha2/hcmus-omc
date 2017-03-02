from django import forms

import django_excel as excel
import pyexcel.ext.xls
import pyexcel.ext.xlsx


class UploadFileForm(forms.Form):
    file = forms.FileField()
