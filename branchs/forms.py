from django import forms
from .models import OCSSC_branch_office
from accounts.models import User


class BranchForm(forms.ModelForm):
	manager = forms.ModelChoiceField(
        empty_label="Select Category",
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True)
	class Meta:
		model = OCSSC_branch_office
		fields = ('name','city','address','head_office','manager',)
		widgets = {
				'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of the branch'}),
				'city':forms.TextInput(attrs={'class':'form-control','placeholder':'city '}),
				'address':forms.TextInput(attrs={'class':'form-control','placeholder':'address'}),
				}
















