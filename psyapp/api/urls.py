from django.conf.urls import include, url

import users

urlpatterns = [
    url(r'^users/', include('users.urls')),
]
