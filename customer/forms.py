from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.db.models.functions import datetime

from customer.models import ServiceRecord, ServiceType
from register.models import User, Car


class UserInfoForm(UserChangeForm):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    gender = forms.ChoiceField(label='性别', choices=GENDER_CHOICES)

    # 隐藏password字段，因为我们将密码修改功能放在另一个页面
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'gender', 'birth_date',  'phone_number',
                  'username')
        labels = {
            'id': 'ID(不可修改)',
            'usename': '用户名',
            'name': '姓名',
            'phone_number': '手机号',
            'birth_date': '出生日期',
            'gender': '性别',
        }
        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
        }




from django.contrib.auth.forms import PasswordChangeForm


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(self.user, *args, **kwargs)
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None



class ServiceApplicationForm(forms.ModelForm):
    # 移除默认设置
    service_type = forms.ModelChoiceField(label='服务类型', queryset=ServiceType.objects.all(), empty_label=None)
    car = forms.ModelChoiceField(label='车型', queryset=Car.objects.all(), empty_label=None)
    description = forms.CharField(label='描述', widget=forms.Textarea)
    datetime = forms.DateTimeField(
        label='申请时间',
        widget=forms.DateTimeInput(attrs={'type': 'datetime'}),
        initial=datetime.datetime.now()
    )
    service_state = forms.IntegerField(label='服务状态', initial=0, widget=forms.HiddenInput())

    class Meta:
        model = ServiceRecord
        fields = ['user', 'service_type', 'car', 'datetime', 'description', 'service_state']
