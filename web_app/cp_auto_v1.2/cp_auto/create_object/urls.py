from django.urls import path, include
from .views import (
    home,
    generate_sids, 
    add_host_commercial, 
    add_host_government,
    add_host_all,
    add_network_commercial,
    add_network_government,
    add_network_all,
    add_network_grp_commercial,
    add_network_grp_government,
    add_network_grp_all,
    copy_network_grp_commercial,
    copy_network_grp_government,
    add_service_commercial,
    add_service_government,
    add_service_all
    )

urlpatterns = [
    path('', home, name='home'),
    path('generate-sids/', generate_sids, name='gensids'),
    path('add-host/commercial/', add_host_commercial, name='add-host-commercial'),
    path('add-host/government/', add_host_government, name='add-host-government'),
    path('add-host/all/', add_host_all, name='add-host-all'),
    path('add-network/commercial/', add_network_commercial, name='add-network-commercial'),
    path('add-network/government/', add_network_government, name='add-network-government'),
    path('add-network/all/', add_network_all, name='add-network-all'),
    path('add-network-grp/commercial/', add_network_grp_commercial, name='add-network-grp-commercial'),
    path('add-network-grp/government/', add_network_grp_government, name='add-network-grp-government'),
    path('add-network-grp/all/', add_network_grp_all, name='add-network-grp-all'),
    path('copy-network-grp/commercial/', copy_network_grp_commercial, name='copy-network-grp-commercial'),
    path('copy-network-grp/government/', copy_network_grp_government, name='copy-network-grp-government'),
    path('add-service/commercial/', add_service_commercial, name='add-service-commercial'),
    path('add-service/government/', add_service_government, name='add-service-government'),
    path('add-service/all/', add_service_all, name='add-service-all'),
]
