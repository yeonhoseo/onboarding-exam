from django.urls import path
from app import views

app_name = "app"
urlpatterns = [
    path("",views.index ,name="index"),    
    path("leadcreate/",views.leadcreate ,name="leadcreate"),
    path("leads/<str:lead_id>",views.lead_detail ,name="lead_detail"),
    path("accounts/",views.account_list,name="account_list"),
    path("accounts/<str:account_id>",views.account_detail,name="account_detail")
]
