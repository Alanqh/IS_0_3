from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.datetime_safe import date

from .models import User, Car


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

    role = forms.ChoiceField(label='角色', choices=ROLE_CHOICES)
    department = forms.ChoiceField(label='部门', choices=DEPARTMENT_CHOICES, required=False)
    last_name = forms.CharField(label='姓')
    first_name = forms.CharField(label='名')
    gender = forms.ChoiceField(label='性别', choices=GENDER_CHOICES)
    birth_date = forms.DateField(
        label='出生年月日',
        widget=forms.DateInput(attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')})
    )
    email = forms.EmailField(label='邮箱')
    phone_number = forms.CharField(label='手机号')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'customer':
            cleaned_data['department'] = 'None'

        return cleaned_data


    class Meta:
        model = User
        fields = (
            'role', 'department', 'last_name', 'first_name', 'gender', 'birth_date', 'email', 'phone_number',
            'username',
            'password1', 'password2')
        verbose_name_plural = '用户'
