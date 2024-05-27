from django.urls import path
from app import views

app_name = "app"
urlpatterns = [
    path("",views.index ,name="index"),
    path("leads/<str:lead_id>",views.lead_detail ,name="lead_detail"),
    path("leadcreate/",views.leadcreate ,name="leadcreate"),
]
