from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _ # https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/#overriding-the-default-fields
 
 
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model() #defaultだとAuth.Userなのを自作のCustomUserに変えないといけない？
        fields = ('username','birthday',)
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget = forms.TextInput(attrs={'type': 'date', 'min':"1900-01-01", 'max':"2020-12-31"})

        
class PasswordUpdateForm(forms.Form):
    password = forms.CharField(
        label = '新しいパスワード',
        strip = False,
        widget=forms.PasswordInput(render_value=True),
    )
    password2 = forms.CharField(
        label = '確認用パスワード',
        strip = False,
        widget=forms.PasswordInput(render_value=True),
    )
    
    def clean_password(self):
        password = self.cleaned_data['password']
        
        if len(password) < 8:
            raise forms.ValidationError('8文字以上で入力してください')
            
        return password
    
    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        
        if password != password2:
            raise forms.ValidationError('2つの入力欄に同じパスワードを入力してください')
    
    