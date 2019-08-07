"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from pages import views
#from pages.views import home_view
from recommend.views import  YesDishes, NoDishes, displayRestaurantsForCuisine, cuisine_input_view, cuisine_dishes_view, cuisine_view, thankyou_view, cuisine_absolute_view

urlpatterns = [
	#path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    #path('create/', product_create_view),
    #path('product/', product_detail_view),
    path('restaurant/', cuisine_dishes_view),
    path('cuisine/', cuisine_view, name='homepage'),
    path('cuisine/displayRestaurantsForCuisine/absoluteCuisineView/', cuisine_absolute_view),
    path('cuisine/thankyou/', thankyou_view),
    #Spath('display/', displayRestaurantsForCuisine),
    path('cuisine/displayRestaurantForCuisine/', displayRestaurantsForCuisine),
    path('cuisine/displayRestaurantsForCuisine/', displayRestaurantsForCuisine),
    #path('cuisine/displayRestaurantsForCuisine/displayDishesForCuisine', displayDishesForCuisine),
    path('cuisine/displayRestaurantsForCuisine/YesDishes', YesDishes),
    path('cuisine/displayRestaurantsForCuisine/NoDishes', NoDishes),
    path('cuisine/displayRestaurantsForCuisine/homepage',cuisine_view )
    #path('cuisine/displayDishesForCuisine/displayDishesForCuisine', displayDishesForCuisine),

]
