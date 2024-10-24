from django.db import models


class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
        help_text="Введите название залоговка",
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите текст записи",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="blog/image",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    public = models.BooleanField(verbose_name="Признак публикации")
    number_of_views = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["title", "created_at", "number_of_views"]

    def __str__(self):
        return self.title
