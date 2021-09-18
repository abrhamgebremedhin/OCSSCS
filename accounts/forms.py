from django import forms 
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import ( ReadOnlyPasswordHashField,
                                        UserCreationForm,
                                        AuthenticationForm,
                                        UsernameField
                                        )
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext as _
from django.contrib.admin.forms import AdminAuthenticationForm

from django_summernote.widgets import SummernoteWidget
from .models import User,Customer,SavingType,BankingHistory
from branchs.models import OCSSC_branch_office
# from accounts.models import Company, CompanyAdmin, Customer
# from company.models import CompanyStaff


# For the Front End Login Form
class FrontLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput())

# Customized Admin Login Form
class AdminLoginForm(AdminAuthenticationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(
        attrs={'placeholder':'Username'}
    ))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Password','autocomplete': 'current-password'}),
    )

# Abstract User Sign Up Form where the other forms extend this form.
class AbstractUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"class":"form-control","placeholder": "Password"},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={"class":"form-control","placeholder": "Re-Type Password"},
    )) 

    class Meta:
        widgets = {
            'first_name': forms.TextInput(attrs={},),
            'last_name': forms.TextInput(attrs={},),
            'username': forms.TextInput(attrs={},),
            'phone_number': forms.TextInput(attrs={},),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_phone_number(self,*args,**kwargs):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number))!=12:
            if '251' not in str(phone_number):
                raise forms.ValidationError("please check your phone number")
        else:
            print("done")
            return phone_number
 
class UserCreationUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('office_branch','first_name','last_name',
            'phone_number','address','city','office_branch',)

    def clean_phone_number(self,*args,**kwargs):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number))!=12:
            if '251' not in str(phone_number):
                raise forms.ValidationError("please check your phone number")
        else:
            print("done")
            return phone_number
        

     
class TransactForm(forms.ModelForm):

    transaction = forms.ChoiceField(required=True,
                          widget=forms.Select(attrs={'type': 'select', "class": "form-control form-control-uniform"}),
                          choices=(('Deposit', 'Deposit'), ('Withdrow', 'Withdrow'), ))

    class Meta:
        model = BankingHistory
        fields = ('amount','transaction')
        

class SavingsTypeForm(forms.ModelForm):

    class Meta:
        model = SavingType
        fields = ('name','detail')
 
        widgets = {
        'name' : forms.TextInput(attrs={"class":"form-control","placeholder":"Name",},),
        'detail' : forms.Textarea(attrs={"class":"form-control","placeholder":"Discription",},),
        }


class CustomerForm(forms.ModelForm):
    office_branch = forms.ModelChoiceField(
        empty_label="Select Category",
        queryset=OCSSC_branch_office.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True)
    savings_type = forms.ModelChoiceField(
        empty_label="Select Category",
        queryset=SavingType.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True)

    class Meta:
        model = Customer
        fields = ('first_name','middle_name','last_name','account_number','savings_type',
                'phone_number','address','city','office_branch','initial_deposit',
                'document','photograph','identification')
 
        widgets = {
        'first_name' : forms.TextInput(attrs={"class":"form-control","placeholder":"First Name",},),
        'middle_name' : forms.TextInput(attrs={"class":"form-control","placeholder":"Middle Name",},),
        'last_name' : forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name",},),
        'account_number':forms.TextInput(attrs={"class":"form-control","placeholder":"Savings Account","id":"Account",},),
        'phone_number':forms.TextInput(attrs={"class":"form-control","placeholder":"Phone number",},),
        'address':forms.TextInput(attrs={"class":"form-control","placeholder":"Address",},),
        'city': forms.TextInput(attrs={"class":"form-control","placeholder":"City",},),
        }

    def clean_phone_number(self,*args,**kwargs):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number))!=12:
            if '251' not in str(phone_number):
                raise forms.ValidationError("please check your phone number")
        else:
            print("done")
            return phone_number

class CustomerEditForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name','middle_name','last_name',
                'phone_number','address','city',)
                
 
        widgets = {
        'first_name' : forms.TextInput(attrs={"class":"form-control","placeholder":"First Name",},),
        'middle_name' : forms.TextInput(attrs={"class":"form-control","placeholder":"Middle Name",},),
        'last_name' : forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name",},),
        'phone_number':forms.TextInput(attrs={"class":"form-control","placeholder":"Phone number",},),
        'address':forms.TextInput(attrs={"class":"form-control","placeholder":"Address",},),
        'city': forms.TextInput(attrs={"class":"form-control","placeholder":"City",},),
        }

    def clean_phone_number(self,*args,**kwargs):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number))!=12:
            if '251' not in str(phone_number):
                raise forms.ValidationError("please check your phone number")
        else:
            print("done")
            return phone_number



class UserCreationForm(AbstractUserCreationForm):
    """ A form is prepared for normal/customer users to regster. Includes all the required
        fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={},
    ))

    office_branch = forms.ModelChoiceField(
        empty_label="Select Category",
        queryset=OCSSC_branch_office.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True)

    user_type = forms.ChoiceField(required=True,
                              widget=forms.Select(attrs={'type': 'select', "class": "form-control form-control-uniform"}),
                              choices=(('is_manager', 'is_manager'), ('is_auditor', 'is_auditor'), 
                                ('is_customer_service', 'is_customer_service'), ('is_system_admin', 'is_system_admin'),))


    class Meta(AbstractUserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','username' ,'phone_number',  
                    'photograph','identification','address','city',
                    'office_branch','qualification_document','date_of_hire',)
        widgets = {
            'first_name': forms.TextInput(attrs={"class":"form-control","placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"class":"form-control","placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"class":"form-control","placeholder": "User Name"},),
            'phone_number': forms.TextInput(attrs={"class":"form-control","placeholder": "+2519-------- ", },),
            'address':forms.TextInput(attrs={"class":"form-control","placeholder": "Address", },),
            'city':forms.TextInput(attrs={"class":"form-control","placeholder": "Ciry", },),
            'date_of_hire':forms.TextInput(attrs={"class":"form-control","placeholder": "First Name", },),
            }

    def clean_phone_number(self,*args,**kwargs):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number))!=12:
            if '251' not in str(phone_number):
                raise forms.ValidationError("please check your phone number")
        else:
            print("done")
            return phone_number

    @transaction.atomic
    def save(self,created_by,date_of_hire):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        user.created_by = created_by
        user.date_of_hire = date_of_hire
        if self.cleaned_data.get("user_type") == "is_manager":
            user.is_manager = True
            user.save()
        if self.cleaned_data.get("user_type") == "is_auditor":
            user.is_auditor = True
            user.save()
        if self.cleaned_data.get("user_type") == "is_customer_service":
            user.is_customer_service = True
            user.save()
        if self.cleaned_data.get("user_type") == "is_system_admin":
            user.is_system_admin = True
            user.save()
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        return user

class AdminCreateUserForm(AbstractUserCreationForm):
    """
    This form is for creating users by super admins
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': "Create Password"},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Re-Type Password'},
    ))
    user_type = forms.ChoiceField(required=True,
                                  widget=forms.Select(
                                      attrs={'type': 'select', "class": "form-control form-control-uniform"}),
                                  choices=(('', 'Select User Types'),
                                            ('admin', 'Super Admin'),
                                            ('contact_person', 'Company Contact Person'),
                                            ('customer', 'Customer'),)
                                  )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if self.cleaned_data.get("user_type") == "admin":
            user.is_staff = True
            user.is_superuser = True
            user.save()
        if self.cleaned_data.get("user_type") == "contact_person":
            user.is_company_admin = True
            user.is_staff = True
            user.save()
            admin_permisstion_list = Permission.objects.all().exclude(
            codename__in=['add_logentry','change_logentry','delete_logentry','view_logentry',
                          'add_permission','change_permission','delete_permission','view_permission',
                          'add_group','change_group','delete_group','view_group',
                          'add_contenttype','change_contenttype','delete_contenttype','view_contenttype',
                          'add_session','change_session','delete_session','view_session'] 
            )
            user.user_permissions.set(admin_permisstion_list)
            user.save()
            comp_admin = CompanyAdmin.objects.create(user=user)
            comp_admin.save()
        elif self.cleaned_data.get("user_type") == "customer":
            user.is_customer = True
            user.save()
            comp_admin = Customer.objects.create(user=user)
            comp_admin.save()
        return user

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('__all__')
        widgets = {
            'permissions': forms.Select(attrs={'class': 'form-control listbox', 'multiple': "multiple"})
        }

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        return group

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password',)
        widgets = {
            'email': forms.EmailInput(
                attrs={}
            )
        }

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



