from django import forms
from .models import User_Detail, CertificateFile, Verify_Certificatefile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Province
from bootstrap_daterangepicker import widgets, fields


class User_DetailForm(forms.ModelForm):
    class Meta:
        model = User_Detail
        fields = ('address', 'province', 'ministry', 'code', 'cal_date', 'password')
        widgets = {
            'address': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'ที่อยู่', 'rows': '1', 'id': 'address'}),
            'province': forms.Select(
                attrs={'class': 'form-control', 'placeholder': '', 'required': 'true', 'id': 'province',
                       'placeholder': 'เลือกจังหวัด'}),
            'ministry': forms.Select(attrs={'class': 'form-control', 'placeholder': '', 'id': 'ministry'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567', 'id': 'code'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true', 'id': 'password_detail'}),
            # 'cal_date': forms.TextInput(attrs={'class': 'form-control', 'name': 'birthday','type':'text',
            #                                    'id': 'cal_date_input',
            #                                    'placeholder': 'เลือกวันที่', 'required': 'true', }),

        }


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_superuser',)
        widgets = {
            'email': forms.EmailInput(
                attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'hospital@mail.com', 'id': 'email'}),
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': "off", 'id': 'username',
                       'name': 'username',
                       'required': 'true'}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password', 'name': 'password',
                       'autocomplete': 'off',
                       'minlength': '8'}),
            'is_superuser': forms.Select(choices=(
                ('0', 'User'),
                ('1', 'Admin'),
            ), attrs={'class': 'form-control', 'placeholder': 'Permission'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hospital@mail.com','id':'email_profile'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }


class CertificateForm(forms.ModelForm):
    class Meta:
        model = CertificateFile
        fields = ('cert', 'hospital')
        widgets = {
            'cert': forms.FileInput(
                attrs={'class': 'form-control form-control-lg', 'id': 'upload_input', 'required': 'true'}),
            # 'hospital': forms.Select(attrs={'class': 'form-control form-control-lg', 'list': 'datalistOptions',
            #                                 'placeholder': "ชื่อโรงพยาบาล", 'type': 'text', 'id': 'datalist_input'})  ,
            'hospital': forms.Select(attrs={
                'class': "js-example-basic-single form-control form-control-lg",
                'name': "state", 'id': 'mySelect2'}),
        }


class Verify_CertificateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Verify_CertificateForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['hospital'].queryset = User.objects.all().exclude(is_superuser=True)
    class Meta:
        model = Verify_Certificatefile
        fields = ('cert', 'hospital', 'editing_message', 'user_create')
        widgets = {
            'cert': forms.FileInput(
                attrs={'class': 'form-control form-control-lg', 'required': 'true', 'id': 'file_verify'}),
            'hospital': forms.Select(attrs={
                'class': "js-example-basic-single form-control form-control-lg",
                'name': "state", 'id': 'mySelect2', 'required': 'true'}),
            'editing_message': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'user_create': forms.TextInput(attrs={'class': 'form-control'})
        }
