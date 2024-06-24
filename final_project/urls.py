
from django.contrib import admin
from django.urls import path
from final_project_app.views import fetch_data,home,THSR_OUPUT,TRA_OUTPUT,METRO

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",home,name="home"),
    path("THSR/",THSR_OUPUT,name="THSR_OUPUT"),
    path("TRA/",TRA_OUTPUT,name="TRA_OUPUT"),
    path("Metro/",METRO, name="Metro_OUTPUT"),
]
