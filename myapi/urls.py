# myapi/urls.py
#from django.urls import include, path
#from rest_framework import routers
from django.conf.urls import url

from . import views

#router = routers.DefaultRouter()
#router.register(r'heroes', views.HeroViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
#urlpatterns = [
#    path('', include(router.urls)),
#    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#]

urlpatterns = [
    url(r'^api/claims$', views.submit_claims),
    url('^api/claims/(?P<cid>[0-9]+)$', views.claims_by_id),
    url(r'^api/claims/list$', views.claims_list)
]