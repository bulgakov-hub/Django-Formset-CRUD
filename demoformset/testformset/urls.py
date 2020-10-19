from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    TestListView,
    TestCreateView,
    TestUpdateView,
    TestDeleteView,
    get_answers,
    get_formset
)


app_name = 'testformset'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
    path('create/', TestCreateView.as_view(), name='create'),
    path('update/<int:pk>/', TestUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TestDeleteView.as_view(), name='delete'),
    path('get-answers/', get_answers, name='get_answers'),
    path('set-params/', get_formset, name='set_params'),
]
