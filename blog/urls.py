from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleDeleteView, ArticleDetailView, ArticleListView, ArticleUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path("create/", ArticleCreateView.as_view(), name="create"),  # это CreateView
    path("", ArticleListView.as_view(), name="list"),  # это ListView
    path("view/<int:pk>/", ArticleDetailView.as_view(), name="view"),  # это DetailView
    path("edit/<int:pk>/", ArticleUpdateView.as_view(), name="edit"),  # это UpdateView
    path("delete/<int:pk>/", ArticleDeleteView.as_view(), name="delete"),  # это DeleteView
]
