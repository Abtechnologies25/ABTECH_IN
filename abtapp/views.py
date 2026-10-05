from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json

def home_view(request):
    return render(request, 'abtapp/home.html', {'active_page': 'home'})

def projects_view(request):
    categories = ProjectCategory.objects.all()
    context = {
        'categories': categories,
        'active_page': 'projects'
    }
    return render(request, 'abtapp/projects.html', context)

def project_category_detail_view(request, category_id):
    """Display projects for a specific category"""
    category = get_object_or_404(ProjectCategory, id=category_id)
    projects = category.projects.all()
    context = {
        'category': category,
        'projects': projects,
        'active_page': 'projects'
    }
    return render(request, 'abtapp/project_category_detail.html', context)

def research_guidance_view(request):
    return render(request, 'abtapp/research_guidance.html', {'active_page': 'research_guidance'})

def training_view(request):
    context = {
        'active_page': 'training'
    }
    return render(request, 'abtapp/training.html', context)

def value_added_courses_view(request):
    vacs = VAC.objects.all().order_by('-from_date')
    college_count = VAC.objects.values('college_name').distinct().count()
    dept_count = VAC.objects.values('department_name').distinct().count()
    context = {
        'vacs': vacs,
        'college_count': college_count,
        'dept_count': dept_count,
        'active_page': 'value_added_courses',
    }
    return render(request, 'abtapp/value_added_courses.html', context)

def gallery_api(request, category_id):
    """API endpoint to fetch gallery images for a category"""
    try:
        category = GalleryCategory.objects.get(id=category_id)
        images = category.images.all()
        
        images_data = []
        for image in images:
            images_data.append({
                'id': image.id,
                'image': image.image.url,
                'name': image.name,
                'alt_text': image.get_seo_alt()
            })
        
        return JsonResponse({
            'success': True,
            'category': category.name,
            'images': images_data
        })
    except GalleryCategory.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Category not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

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

def branch_nagercoil_view(request):
    return render(request, 'abtapp/branch_nagercoil.html', {'active_page': 'our_branches'})

def branch_tirunelveli_view(request):
    return render(request, 'abtapp/branch_tirunelveli.html', {'active_page': 'our_branches'})

def branch_chennai_view(request):
    return render(request, 'abtapp/branch_chennai.html', {'active_page': 'our_branches'})

def branch_pudukkottai_view(request):
    return render(request, 'abtapp/branch_pudukkottai.html', {'active_page': 'our_branches'})

def branch_marthandam_view(request):
    return render(request, 'abtapp/branch_marthandam.html', {'active_page': 'our_branches'})

def contact_us_view(request):
    return render(request, 'abtapp/contact_us.html', {'active_page': 'contact_us'})

def consultancy_projects_view(request):
    projects = ConsultancyProject.objects.all().order_by('-id')
    context = {
        'projects': projects,
        'active_page': 'consultancy_projects',
    }
    return render(request, 'abtapp/consultancy_projects.html', context)

def funded_projects_view(request):
    projects = FundedProject.objects.all().order_by('-id')
    context = {
        'projects': projects,
        'active_page': 'funded_projects',
    }
    return render(request, 'abtapp/funded_projects.html', context)


