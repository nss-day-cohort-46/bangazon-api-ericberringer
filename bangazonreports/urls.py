from django.urls import path
from .views import favoritebyuser_list

urlpatterns = [
    path('reports/userfavs', favoritebyuser_list),
]