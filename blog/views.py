from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.forms import ArticleForm
from blog.models import Article
from services.mixins import StatisticMixin


class ArticleViewMixin:
    """Миксин для формы статьи"""

    model = Article
    form_class = ArticleForm
    template_name = "blog/article_form.html"


class ArticleCreateView(
    ArticleViewMixin, LoginRequiredMixin, CreateView
):  # создаем класс BlogCreateView, который наследуется от CreateView
    """Создание статьи"""

    login_url = reverse_lazy("user:login")
    success_url = reverse_lazy("blog:list")  # указываем URL, на который будет перенаправлен пользователь после


class ArticleUpdateView(
    ArticleViewMixin, UpdateView
):  # создаем класс BlogUpdateView, который наследуется от UpdateView
    """Редактирование статьи"""

    def get_success_url(self):  # переопределяем метод get_success_url
        return reverse("blog:view", kwargs={"pk": self.get_object().pk})
        # возвращаем URL, на который будет перенаправлен


class ArticleListView(StatisticMixin, ListView):  # создаем класс BlogListView, который наследуется от ListView
    """Список статей"""

    model = Article  # указываем модель, с которой будет работать наш класс
    template_name = "blog/article_list.html"  # указываем имя шаблона, который будет использоваться
    extra_context = {"title": "Список статей"}  # Добавление дополнительного контекста на страницу

    def get_queryset(self, *args, **kwargs):  # тут мы переопределяем метод get_queryset
        """Получаем queryset и фильтруем его по признаку публикации"""
        queryset = (
            super().get_queryset().order_by(*args, **kwargs)
        )  # вызываем родительский метод get_queryset и сортируем его
        queryset = queryset.filter(published=True)  # фильтруем queryset по признаку публикации
        return queryset  # возвращаем отфильтрованный queryset


class ArticleDetailView(DetailView):  # создаем класс BlogDetailView, который наследуется от DetailView
    """Просмотр статьи"""

    model = Article
    template_name = "blog/article_detail.html"  # указываем имя шаблона, который будет использоваться


class ArticleDeleteView(DeleteView):
    """Удаление статьи"""

    model = Article
    success_url = reverse_lazy("blog:list")  # указываем URL, на который будет перенаправлен пользователь после
    template_name = "blog/article_confirm_delete.html"  # указываем имя шаблона, который будет использоваться
