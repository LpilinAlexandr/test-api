from django.urls import path, re_path, include
from . import views as api


app_name = 'api'

urlpatterns = []

urlpatterns.append(
    path('pets', include([
        path('', api.PetView.as_view()),
        re_path(r'^/(?P<pet_id>[0-9a-f-]+)/photo$', api.PhotoUploadView.as_view()),
    ]))
)
