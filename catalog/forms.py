from django.forms import ModelForm
from catalog.models import Product
from django.core.exceptions import ValidationError


class ProductForm(ModelForm):
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

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Настройка атрибутов виджета для поля 'name'
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите наименование продукта",  # Текст подсказки внутри поля
            }
        )

        # Настройка атрибутов виджета для поля 'description'
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите описание продукта",  # Текст подсказки внутри поля
            }
        )

        # Настройка атрибутов виджета для поля 'price'
        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите цену продукта",  # Текст подсказки внутри поля
            }
        )

        # Настройка атрибутов виджета для поля 'category'
        self.fields["category"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Укажите категорию продукта",  # Текст подсказки внутри поля
            }
        )
