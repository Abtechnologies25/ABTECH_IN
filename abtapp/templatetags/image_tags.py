"""
Custom template tags for image optimization and lazy loading
"""

from django import template
from django.utils.safestring import mark_safe
import os

register = template.Library()


@register.filter
def lazy_load_image(image_path, alt_text="Image"):
    """
    Generate lazy-loaded image HTML with blur-up effect
    Usage: {{ image_path|lazy_load_image:"Alt text" }}
    """
    html = f'''
    <img 
        src="{image_path}" 
        alt="{alt_text}"
        loading="lazy"
        decoding="async"
        class="lazy-image"
        data-src="{image_path}"
    />
    '''
    return mark_safe(html)


@register.filter
def responsive_image(image_url, size="medium"):
    """
    Generate responsive image with srcset
    Sizes: small (300px), medium (500px), large (800px), hero (1200px)
    """
    base_url = image_url.rsplit('.', 1)[0]
    extension = image_url.rsplit('.', 1)[1]
    
    sizes_map = {
        'small': '300w',
        'medium': '500w',
        'large': '800w',
        'hero': '1200w'
    }
    
    srcset = f"{base_url}-small.{extension} 300w, {base_url}.{extension} 500w, {base_url}-large.{extension} 800w"
    
    html = f'''
    <img 
        src="{image_url}"
        srcset="{srcset}"
        sizes="{sizes_map.get(size, '100vw')}"
        loading="lazy"
        decoding="async"
        alt="Responsive Image"
        class="responsive-img"
    />
    '''
    return mark_safe(html)


@register.filter
def webp_image(image_url, alt_text="Image"):
    """
    Generate WebP image with fallback to original format
    WebP is 25-30% smaller than JPEG
    """
    base_url = image_url.rsplit('.', 1)[0]
    extension = image_url.rsplit('.', 1)[1]
    webp_url = f"{base_url}.webp"
    
    html = f'''
    <picture>
        <source srcset="{webp_url}" type="image/webp">
        <img 
            src="{image_url}" 
            alt="{alt_text}"
            loading="lazy"
            decoding="async"
            class="lazy-image"
        />
    </picture>
    '''
    return mark_safe(html)


@register.simple_tag
def lazy_load_gallery(image_list):
    """
    Generate lazy-loaded gallery for multiple images
    """
    html = '<div class="lazy-gallery">'
    for image in image_list:
        html += f'''
        <img 
            src="{image.image.url}" 
            alt="{image.get_seo_alt()}"
            loading="lazy"
            decoding="async"
            class="gallery-image"
        />
        '''
    html += '</div>'
    return mark_safe(html)
