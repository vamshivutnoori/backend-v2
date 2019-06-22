from django.contrib import admin
from django.urls import path, include
from mysite.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('CVEsearch/',views.cvesearch,name='CVE'),
    path('result/',views.output,name='script'),
	path('products/',views.products,name='products'),
	path('subscriptions/',views.subscriptions,name='subscriptions'),
	path('manual_sub/',views.direct_sub,name='manual_sub'),	
	path('add_prod/',views.add_prod,name="add_prod"),

]

views.hello(repeat=60000,repeat_until=None)