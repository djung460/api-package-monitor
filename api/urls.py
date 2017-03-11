from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
        # mobile facing
        url(r'^api/login$',views.login),
        url(r'^api/signup$',views.signup),
        url(r'^api/acknowledge$',views.acknowledge),
        url(r'^api/requestcheck$',views.requestcheck),
        url(r'^api/viewlog',views.viewlog),

        # package monitor facing
        url(r'^api/isack$',views.isack),
        url(r'^api/requestopen$',views.requestopen),
        url(r'^api/isapproved$',views.isapproved),
]

urlpatters = format_suffix_patterns(urlpatterns)
