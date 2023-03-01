from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('tsla/', views.tslaStock, name="tesla"),
    path('aapl/', views.aaplStock, name="apple"),
    path('amzn/', views.amznStock, name="amazon"),
    path('goog/', views.googStock, name="google"),
    path('msft/', views.msftStock, name="microsoft"),
    path('nvda/', views.nvdaStock, name="nvda"),
    path("register/", views.register, name="register"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("stock_request/", views.stock_request, name="stock_request")
    # path('signup/', views.my_form, name="signup"),
    # path('register/', views.register, name='register'),
    # path('login/', views.login_user, name='login_user'),
    # path('logout/', views.logout_user, name='logout_user'),
    # path('student_register/', views.student_register.as_view(), name='student_register'),
    # path('teacher_register/', views.teacher_register.as_view(), name='teacher_register')
]