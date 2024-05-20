from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url
from . import views

router = routers.DefaultRouter()
router.register(r'games', views.GameViewset)
router.register(r'active-games', views.ActiveGameViewset)
#router.register(r'user-profile', views.UserViewset)
urlpatterns = router.urls

urlpatterns += [
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^profile/$', views.UserView.as_view(), name='profile'),
    # url(r'^active-game-log/(?P<pk>\d+)/$', views.UserView.as_view(), name='profile'),

]