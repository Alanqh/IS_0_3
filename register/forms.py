from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.datetime_safe import date

from .models import User


class UserCreationForms(UserCreationForm):
    ROLE_CHOICES = (
        ('customer', '客户'),
        ('staff', '员工'),
    )
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    DEPARTMENT_CHOICES = (
        ('aftersales', '售后'),
        ('inventory', '库存'),
        ('finance', '财务'),
        ('hr', '人力资源'),
        ('customer service', '客服'),
    )

    role = forms.ChoiceField(label='角色', choices=ROLE_CHOICES, widget=forms.Select(attrs={'onchange': 'toggleDepartment()'}))
    department = forms.ChoiceField(label='部门', choices=DEPARTMENT_CHOICES, required=False)
    name = forms.CharField(label='姓名')
    gender = forms.ChoiceField(label='性别', choices=GENDER_CHOICES)
    birth_date = forms.DateField(
        label='生日',
        widget=forms.DateInput(attrs={'type': 'date', 'max': date.today()}),
    )
    phone_number = forms.CharField(label='手机号')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'customer':
            cleaned_data['department'] = 'None'

        return cleaned_data

    class Meta:
        model = User
        fields = (
            'role', 'department', 'name', 'gender', 'birth_date', 'phone_number',
            'username',
            'password1', 'password2')
        verbose_name_plural = '用户'
