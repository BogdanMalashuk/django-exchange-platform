from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('ads/create/', views.ad_create, name='ad_create'),
    path('ads/<int:ad_id>/edit/', views.ad_edit, name='ad_edit'),
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ads/<int:ad_id>/delete', views.ad_delete, name='ad_delete'),
    path('ads/<int:ad_id>/propose/', views.propose_exchange, name='propose_exchange'),
    path('user/incoming/', views.incoming_proposals, name='incoming'),
    path('user/outgoing/', views.outgoing_proposals, name='outgoing'),
    path('proposals/<int:proposal_id>/accept/', views.accept_proposal, name='accept_proposal'),
    path('proposals/<int:proposal_id>/reject/', views.reject_proposal, name='reject_proposal'),
]
