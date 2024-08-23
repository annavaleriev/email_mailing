from django.db import models

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    slug = models.SlugField()
    body = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(verbose_name="Превью", upload_to="blog/", **NULLABLE)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    published = models.BooleanField(verbose_name="Признак публикации", default=True)
    views = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self.title

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
