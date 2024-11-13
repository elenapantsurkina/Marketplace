from django.forms import ModelForm
from catalog.models import Product
from django.core.exceptions import ValidationError
from django.forms.fields import BooleanField


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    forbidden_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        if name:
            for word in self.forbidden_words:
                if word in name.lower():
                    self.add_error("name", f'Name не может содержать слово "{word}"')

        if description:
            for word in self.forbidden_words:
                if word in description.lower():
                    self.add_error(
                        "description", f'Description не может содержать слово "{word}"'
                    )

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price
