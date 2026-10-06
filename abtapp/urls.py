from django.urls import path
from . import views

urlpatterns = [
    path('robots.txt', views.robots_txt_view, name='robots_txt'),
    path('', views.home_view, name='home'),
    path('projects/', views.projects_view, name='projects'),
    path('projects/<int:category_id>/', views.project_category_detail_view, name='project_category_detail'),
    path('research-guidance/', views.research_guidance_view, name='research_guidance'),
    path('training/', views.training_view, name='training'),
    path('value-added-courses/', views.value_added_courses_view, name='value_added_courses'),
    path('products/', views.products_view, name='products'),
    path('mou/', views.mou_view, name='mou'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('videos/', views.videos_view, name='videos'),
    path('career/', views.career_view, name='career'),
    path('our-team/', views.our_team_view, name='our_team'),
    path('our-branches/', views.our_branches_view, name='our_branches'),
    path('our-branches/nagercoil/', views.branch_nagercoil_view, name='branch_nagercoil'),
    path('our-branches/tirunelveli/', views.branch_tirunelveli_view, name='branch_tirunelveli'),
    path('our-branches/chennai/', views.branch_chennai_view, name='branch_chennai'),
    path('our-branches/pudukkottai/', views.branch_pudukkottai_view, name='branch_pudukkottai'),
    path('our-branches/marthandam/', views.branch_marthandam_view, name='branch_marthandam'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('services/consultancy-projects/', views.consultancy_projects_view, name='consultancy_projects'),
    path('services/funded-projects/', views.funded_projects_view, name='funded_projects'),
    # API endpoints

    path('api/gallery/<int:category_id>/', views.gallery_api, name='gallery_api'),
]
