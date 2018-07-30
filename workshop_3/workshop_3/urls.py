"""workshop_3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rbms.views import new_room, modify_room, delete_room, show_room,\
    view_all, room_search, reserve_room

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/new', new_room, name="new_room"),
    re_path(
        r"""^room/modify/(?P<id>(\d)+)$""", modify_room, name="modify_room"
    ),
    re_path(
        r"""^room/delete/(?P<id>(\d)+)$""", delete_room, name="delete_room"
    ),
    re_path(r"""^room/(?P<id>(\d)+)$""", show_room, name="show_room"),
    path('', view_all, name="view_all"),
    path("search/", room_search, name="search"),
    re_path(
        r"""^room/reservation/(?P<id>(\d)+)$""",
        reserve_room, name="reserve_room"
    ),
]
