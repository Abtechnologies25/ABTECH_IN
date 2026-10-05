import os
import re
import smtplib

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
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
    if request.method == 'GET':
        return render(request, 'abtapp/career.html', {'active_page': 'career'})
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)

    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    resume = request.FILES.get('resume')

    if not full_name or len(full_name) > 200:
        return JsonResponse({'success': False, 'error': 'Enter your name (up to 200 characters).'}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'success': False, 'error': 'Enter a valid email address.'}, status=400)
    if not re.fullmatch(r'\d{10}', phone):
        return JsonResponse({'success': False, 'error': 'Enter a valid 10-digit phone number.'}, status=400)
    if resume is None:
        return JsonResponse({'success': False, 'error': 'Please upload your resume.'}, status=400)
    if resume.size > 5 * 1024 * 1024:
        return JsonResponse({'success': False, 'error': 'Resume must be 5MB or smaller.'}, status=400)
    if os.path.splitext(resume.name)[1].lower() not in {'.pdf', '.doc', '.docx'}:
        return JsonResponse({'success': False, 'error': 'Upload a PDF or DOC/DOCX resume.'}, status=400)

    sender = settings.DEFAULT_FROM_EMAIL
    if not settings.EMAIL_HOST or not sender:
        return JsonResponse({
            'success': False,
            'error': 'Email delivery is not configured. Please contact us directly.'
        }, status=503)

    message = EmailMessage(
        subject=f'Career application from {full_name}',
        body=f'Name: {full_name}\nEmail: {email}\nPhone: {phone}',
        from_email=sender,
        to=['abtechchennai@gmail.com'],
        reply_to=[email],
    )
    safe_filename = os.path.basename(resume.name).replace('\r', '').replace('\n', '')
    message.attach(safe_filename, resume.read(), resume.content_type or 'application/octet-stream')

    try:
        sent_count = message.send(fail_silently=False)
    except (OSError, smtplib.SMTPException):
        return JsonResponse({
            'success': False,
            'error': 'We could not send your application right now. Please try again later.'
        }, status=503)
    if sent_count != 1:
        return JsonResponse({
            'success': False,
            'error': 'We could not send your application right now. Please try again later.'
        }, status=503)

    return JsonResponse({'success': True})

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

