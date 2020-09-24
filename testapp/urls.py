from django.urls import path

from testapp import views

urlpatterns = [
    path("view.css", views.CssView.as_view()),
]
