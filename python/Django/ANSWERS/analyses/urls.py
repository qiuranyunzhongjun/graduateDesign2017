from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'measures', views.MeasureViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^index/',views.index,name='index'),
    url(r'^(?P<patient_id>[0-9]+)/answers/',views.answers,name='answers'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]