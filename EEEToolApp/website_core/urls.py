from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path(r'^delete_files', views.clear_files, name="delete_excel_files"),
    path(r'^calculate_files', views.calculate_and_download, name="calculate"),
    path(r'^download/(?P<filename>[\w-]+)/s', views.download, name="download")

]
