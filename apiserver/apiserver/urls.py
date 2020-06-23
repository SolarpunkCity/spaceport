from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .api import views
from . import secrets

IPN_ROUTE = r'^ipn/{}/'.format(secrets.IPN_RANDOM)
ADMIN_ROUTE = '{}/admin/'.format(secrets.ADMIN_RANDOM)

router = routers.DefaultRouter()
router.register(r'door', views.DoorViewSet, basename='door')
router.register(r'lockout', views.LockoutViewSet, basename='lockout')
router.register(r'cards', views.CardViewSet, basename='card')
router.register(r'stats', views.StatsViewSet, basename='stats')
router.register(r'search', views.SearchViewSet, basename='search')
router.register(r'members', views.MemberViewSet, basename='members')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'history', views.HistoryViewSet, basename='history')
router.register(r'sessions', views.SessionViewSet, basename='session')
router.register(r'training', views.TrainingViewSet, basename='training')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'charts/membercount', views.MemberCountViewSet, basename='membercount')
router.register(r'charts/signupcount', views.SignupCountViewSet, basename='signupcount')
router.register(r'charts/spaceactivity', views.SpaceActivityViewSet, basename='spaceactivity')
#router.register(r'me', views.FullMemberView, basename='fullmember')
#router.register(r'registration', views.RegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path(ADMIN_ROUTE, admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^password/reset/$', views.PasswordResetView.as_view(), name='rest_password_reset'),
    url(r'^password/reset/confirm/$', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.null_view, name='password_reset_confirm'),
    url(r'^password/change/', views.PasswordChangeView.as_view(), name='rest_password_change'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^registration/', views.RegistrationView.as_view(), name='rest_name_register'),
    url(r'^user/', views.UserView.as_view(), name='user'),
    url(r'^ping/', views.PingView.as_view(), name='ping'),
    url(r'^paste/', views.PasteView.as_view(), name='paste'),
    url(r'^backup/', views.BackupView.as_view(), name='backup'),
    url(IPN_ROUTE, views.IpnView.as_view(), name='ipn'),
]
