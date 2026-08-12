from django.shortcuts import render
from .models import *
def home_view(request):
    return render(request, 'abtapp/home.html', {'active_page': 'home'})

def projects_view(request):
    return render(request, 'abtapp/projects.html', {'active_page': 'projects'})

def research_guidance_view(request):
    return render(request, 'abtapp/research_guidance.html', {'active_page': 'research_guidance'})

def training_workshop_view(request):
    return render(request, 'abtapp/training_workshop.html', {'active_page': 'training_workshop'})

def products_view(request):
    return render(request, 'abtapp/products.html', {'active_page': 'products'})

def mou_view(request):
    mous = MoU.objects.all().order_by('MoU_NO')
    context = {
        'mous': mous,
        'active_page': 'mou',
    }
    return render(request, 'abtapp/mou.html', context)

def gallery_view(request):
    categories = GalleryCategory.objects.prefetch_related('images').all()
    context = {
        'categories': categories,
        'active_page': 'gallery',
    }
    return render(request, 'abtapp/gallery.html', context)

def videos_view(request):
    videos = Video.objects.all().order_by('UPLOADED_DATE', 'CODE')
    context = {
        'videos': videos,
        'active_page': 'videos',
    }
    return render(request, 'abtapp/videos.html', context)

def career_view(request):
    return render(request, 'abtapp/career.html', {'active_page': 'career'})

def our_team_view(request):
    return render(request, 'abtapp/our_team.html', {'active_page': 'our_team'})

def our_branches_view(request):
    return render(request, 'abtapp/our_branches.html', {'active_page': 'our_branches'})

def contact_us_view(request):
    return render(request, 'abtapp/contact_us.html', {'active_page': 'contact_us'})
