from django.urls import path
from . import views
urlpatterns=[
    path('',views.root),
    path('show_sign_in_form',views.showSignInForm),
    path('show_create_account_form',views.showCreateAccountForm),
    path('show_cart_form',views.showCartForm),
    path('add_category', views.addCategory)
]