from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)] # 列表生成式


class CartUpdateBookForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class CartAddBookForm(forms.Form):
    quantity = forms.IntegerField(
        label="数量",
        min_value=1,
        initial=1,
    )
