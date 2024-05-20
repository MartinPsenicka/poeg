 from django.conf.urls import url, include

from . import views as core_views
from ..payments import views as payment_views
from ..users.views import my_profile_view

res = dict(
    game='(?P<game_id>\d+)',
    transaction='(?P<transaction_id>\d+)',
    secret='1f206029f97fdc7f380cde6a7cfd68c0',
)

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', core_views.homepage_view, name='homepage'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^me/$', my_profile_view, name='my_profile'),
    url(r'^activate/%(game)s/$' % res, core_views.activate_game, name='activate_game'),

    # TODO: looks unused
    # url(r'^payment/(?P<game_id>\d+)/$', payment_views.confirm_payment, name='payment'),

    url(r'^bankwire/%(game)s/$' % res, payment_views.bankwire_payment, name='bankwire'),

    url(r'^gopay/%(game)s/$' % res, payment_views.gopay_payment, name='payment-gopay'),
    url(
        r'^gopay/return/%(secret)s/%(transaction)s/$' % res,
        payment_views.gopay_return,
        name='payment-gopay-return'
    ),
    url(
        r'^gopay/notify/%(secret)s/%(transaction)s/$' % res,
        payment_views.gopay_notify,
        name='payment-gopay-notify'
    ),

    # voucher admin
    url(
        r'^me/voucher_update/$',
        payment_views.update_voucher_by_dealer,
        name='voucher_update'
    ),

    # game play
    url(r'^game/(?P<active_game_id>\d+)/', include('poeg.apps.games.urls')),

]
