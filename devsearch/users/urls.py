from django.urls import path
from . import views


urlpatterns = [
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("register/",views.register_user,name="register"),


    path("", views.profiles,name="profiles" ),
    path("profile/<str:pk>/", views.profile,name="profile" ),
    path("account/<str:pk>/", views.user_account,name="account" ),
    path("skill_edit/<str:pk>/", views.skill_edit,name="skill_edit" ),
    path("skill_create/", views.skill_create,name="skill_create" ),
    path("skill_delete/<str:pk>/", views.skill_delete,name="skill_delete" ),
    path("skill_delete/<str:pk>/", views.skill_delete,name="skill_delete" ),
    path("edit_account/", views.edit_account,name="edit_account" ),
]