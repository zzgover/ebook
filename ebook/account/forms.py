import re
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UsernameField
import unicodedata
from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _




# 自定义验证规则
def mobile_validate(value):
    mobile_re =re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class UserProfileForm(forms.Form):
    real_name = forms.CharField(
        label="真实姓名",
        required=True,
        error_messages={
            "required": "该字段不能为空",
        },
        widget=widgets.TextInput(attrs={'class': "form-control",
                                        'placeholder': '真实姓名'})
    )
    # 使用自定义验证规则
    phone =forms.CharField(
        label="电话号码",
        required=True,
        validators=[mobile_validate, ],
        widget=widgets.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': '电话号码'}),error_messages = {
        "required": "该字段不能为空",
    }
    )






    address = forms.CharField(
        label="地址",
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control",
                                        'placeholder': '地址'}),
        error_messages={
            "required": "该字段不能为空",
        }
    )


# class UsernameField(forms.CharField):
#     def to_python(self, value):
#
#         return unicodedata.normalize('NFKC', super(UsernameField,
#                                                    self).to_python(value))
#
#
# # 修改 auth 组件下的 usercreateForm
# class UserCreationForm(forms.ModelForm):
#     """
#     A form that creates a user, with no privileges, from the given username and
#     password.
#     """
#     error_messages = {
#         'password_mismatch': _("两次输入的密码不一致."),
#     }
#     password1 = forms.CharField(
#         label=_("密码"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),  # 添 加 了Bootstrap表单样式'class': 'form-control'
#     help_text = password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("确认密码"),
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),  # 添加了 Bootstrap表单样式'class': 'form-control'
#     strip = False,
#             help_text = _("请输入与上面一样的密码."),
#     )
#
#     class Meta:
#         model = User
#
#     fields = ("username",)
#     field_classes = {'username': UsernameField}
#
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
#
#         if self._meta.model.USERNAME_FIELD in self.fields:
#             self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True,
#                                                                   'class': 'form-control'})
#
#
# # 添加了 Bootstrap 表单样式'class': 'form-control'
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#
#
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#     )
#         self.instance.username = self.cleaned_data.get('username')
#         password_validation.validate_password(self.cleaned_data.get('password2'),
#                                       self.instance)
#         return password2
#
#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
