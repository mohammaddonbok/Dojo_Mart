from django.urls import path
from . import views
urlpatterns=[
    path('',views.root),
    path('show_sign_in_form',views.showSignInForm),
    path('show_create_account_form',views.showCreateAccountForm),
    path('show_cart_form',views.showCartForm),
    path('add_category', views.addCategory),
    path('add_user',views.addUser),
    path('validateEmailByAjax',views.validateEmailByAjax,name="validateEmailByAjax"),
    path('validateFirstNameByAjax',views.validateFirstNameByAjax,name="validateFirstNameByAjax"),
    path('validateLastNameByAjax',views.validateLastNameByAjax,name="validateLastNameByAjax"),
    path('validatePasswordByAjax',views.validatePasswordByAjax,name="validatePasswordByAjax"),
    path('logout',views.logout),
    path('signin',views.signin),
    path('show_category_product/<int:category_id>',views.showCatgeoryProducts),
    path('admin', views.showadminpage),
    path('edit_product_form/<int:id>', views.edit_product_form),
    path('edit_product/<int:id>', views.edit_product),
    path('suggestion',views.suggestion, name='suggestion'),
    path('add_product_form', views.add_product_form),
    path('add_product',views.add_product)
]

