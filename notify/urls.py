from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import NotifyViewSet, RecipientViewSet
from .apps import NotifyConfig


app_name = NotifyConfig.name

router = DefaultRouter()
router.register('notify', NotifyViewSet, basename='notify')
router.register('recipient', RecipientViewSet, basename='recipient')

recipient_create = RecipientViewSet.as_view({"post": "create"})
recipient_detail = RecipientViewSet.as_view({"get": "retrieve"})
recipient_update = RecipientViewSet.as_view({"put": "update", "patch": "partial_update"})
recipient_delete = RecipientViewSet.as_view({"delete": "destroy"})


urlpatterns = [
    path('recipient/create/', recipient_create, name="recipient_create"),
    path('recipient/<int:pk>/', recipient_detail, name="recipient_detail"),
    path('recipient/<int:pk>/update/', recipient_update, name="recipient_update"),
    path('recipient/<int:pk>/delete', recipient_delete, name="recipient_destroy"),
]+router.urls
