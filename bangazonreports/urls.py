from django.urls import path
from .views import favoritebyuser_list, unpaidorders_list, completedorders_list, inexpensiveproducts_list, expensiveproducts_list

urlpatterns = [
    path('reports/userfavs', favoritebyuser_list),
    path('reports/unpaidorders', unpaidorders_list),
    path('reports/completedorders', completedorders_list),
    path('reports/inexpensiveproducts', inexpensiveproducts_list),
    path('reports/expensiveproducts', expensiveproducts_list),
]