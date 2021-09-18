from django import forms
from .models import Loan_type,Loan_processing,Documents,Conditions
from accounts.models import User


class LoansTypeForm(forms.ModelForm):

    class Meta:
        model = Loan_type
        fields = ('name','detail')
 
        widgets = {
        'name' : forms.TextInput(attrs={"class":"form-control","placeholder":"Name",},),
        'detail' : forms.Textarea(attrs={"class":"form-control","placeholder":"Discription",},),
        }

class LoanApplication(forms.ModelForm):
	loan_type = forms.ModelChoiceField(
        empty_label="Select Category",
        queryset=Loan_type.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True)

	class Meta:
		model = Loan_processing
		fields = ('current_financial_info','business_plane','Financial_aid_required','loan_type')

		widget = {
		'Financial_aid_required ': forms.TextInput(attrs={'class':'form-control','placeholder':'Amount the client is requesting'})
		}

class LoanApplicationEdit(forms.ModelForm):

    class Meta:
        model = Loan_processing
        fields = ('loan_type','Financial_aid_required')
        widget = {

        }