from django.urls import path
from .views import favoritebyuser_list, unpaidorders_list

urlpatterns = [
    path('reports/userfavs', favoritebyuser_list),
    path('reports/unpaidorders', unpaidorders_list),
]