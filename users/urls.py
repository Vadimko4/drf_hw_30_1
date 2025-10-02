from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet

app_name = UsersConfig.name


router = SimpleRouter()
router.register("payments", PaymentViewSet)

urlpatterns = []
urlpatterns += router.urls
