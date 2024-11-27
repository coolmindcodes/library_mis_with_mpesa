"""
URL configuration for library_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from library_app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('borrowed/books', views.borrowed_books, name='borrowed_books'),
    path('issue/<int:book_id>', views.issue, name='issue'),
    path('return/<int:borrowed_id>', views.return_item, name='return_item'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('pie', views.pie_chart_data, name='pie_chart_data'),
    path('area', views.area_chart_data, name='area_chart_data'),
    path('bar', views.bar_chart_data, name='bar_chart_data'),
    path('fine/payment/<int:id>', views.pay_fine, name='pay_fine'),
    path('callback', views.callback, name='callback'),
    path('returns', views.returns, name='returns'),
    path('login', views.login_user, name='login'),
    path('logout', views.signout_user, name='logout'),
    path('admin/', admin.site.urls),
]
