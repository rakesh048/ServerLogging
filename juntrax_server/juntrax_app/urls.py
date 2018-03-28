from django.conf.urls import url, include
from rest_framework import routers
from juntrax_app.views import ServerUptime,RequestLogging,GoogleReverseGeocoding,LimitChange

router = routers.DefaultRouter()
router.register(r'serveruptime', ServerUptime,base_name='ServerUptime')
router.register(r'requestlogging', RequestLogging,base_name='requestlogging')
router.register(r'googlereversegeocoding', GoogleReverseGeocoding,base_name='GoogleReverseGeocoding')
router.register(r'limitchange', LimitChange,base_name='LimitChange')

urlpatterns = [
    url(r'^', include(router.urls)),
]