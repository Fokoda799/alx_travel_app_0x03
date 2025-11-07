from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingsViewSet, BookingsViewSet, ReviewViewSet, initiate_payment, verify_payment


router = DefaultRouter()

router.register(r'listings', ListingsViewSet, basename='listings')
router.register(r'bookings', BookingsViewSet, basename='bookings')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
  path('', include(router.urls)),
  path('bookings/<int:booking_id>/initiate-payment/', initiate_payment, name='initiate-payment'),
  path('payments/<str:transaction_id>/verify/', verify_payment, name='verify-payment'),
]
