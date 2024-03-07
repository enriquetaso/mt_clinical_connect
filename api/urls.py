from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HospitalViewSet, ContactView

router = DefaultRouter()
router.register(r"hospitals", HospitalViewSet)

urlpatterns = [
    path("contacts/", ContactView.as_view(), name="contact-list"),
]
urlpatterns += router.urls
