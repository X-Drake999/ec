from django import forms
from shop.models import *


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'category', 'price', 'stock', 'available')
        labels = {
            'name': '名前',
            'image': '画像'
        }
        help_texts = {
            'name': '名前を入力',
            'image': '商品画像のアップロード'
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder': '説明文を入力', 'cols':50})
        
class ProductSelectForm(forms.Form):
    CHOICES = []
    
    for product in Product.objects.all():
        #tmp_lis = [product, product.name]
        #tmp_tuple = tuple(tmp_lis)
        CHOICES.append([product, product.name])
      
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())

