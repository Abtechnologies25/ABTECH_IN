"""
Image Optimization Middleware for AB Technologies
Implements compression, caching headers, and performance improvements
"""

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import os


class ImageOptimizationMiddleware(MiddlewareMixin):
    """
    Middleware to add proper caching headers for images
    and optimize image delivery
    """
    
    def process_response(self, request, response):
        # Add cache headers for static images (30 days)
        if request.path.startswith('/static/') and any(
            request.path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        ):
            response['Cache-Control'] = 'public, max-age=2592000'  # 30 days
            response['X-Content-Type-Options'] = 'nosniff'
        
        # Add cache headers for media images (7 days)
        if request.path.startswith('/media/') and any(
            request.path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        ):
            response['Cache-Control'] = 'public, max-age=604800'  # 7 days
            response['X-Content-Type-Options'] = 'nosniff'
        
        return response


class ImageCompressionSettings:
    """
    Configuration for image compression and optimization
    """
    
    # SORL-thumbnail configuration
    THUMBNAIL_SETTINGS = {
        'SORL_THUMBNAIL_DEBUG': False,
        'THUMBNAIL_DEBUG': False,
        'THUMBNAIL_ENGINE': 'sorl.thumbnail.engines.pil_engine.Engine',
        'THUMBNAIL_FORMAT': 'JPEG',
        'THUMBNAIL_KEY_PREFIX': 'sorl-thumbnail',
        'THUMBNAIL_PRESERVE_FORMAT': True,
        'THUMBNAIL_QUALITY': 95,  # High quality
        'THUMBNAIL_COLORSPACE': None,
        'THUMBNAIL_UPSCALE': True,
        'THUMBNAIL_PROGRESSIVE': 100,
        'THUMBNAIL_ORIENTATION': True,
        'THUMBNAIL_ALIAS': {
            # Define image sizes for different use cases
            'small': {'size': (300, 300), 'crop': 'center'},
            'medium': {'size': (500, 500), 'crop': 'center'},
            'large': {'size': (800, 800), 'crop': 'center'},
            'thumbnail': {'size': (200, 200), 'crop': 'center'},
            'hero': {'size': (1200, 600), 'crop': 'center'},
        }
    }


# Recommended Django Settings to add to settings.py:
"""
# Add to settings.py for image optimization

# 1. Pillow/PIL Configuration
INSTALLED_APPS = [
    ...
    'sorl.thumbnail',  # For thumbnail generation
    'corsheaders',  # For CORS if using external CDN
]

# 2. Image Compression Settings
if not DEBUG:
    # Production image optimization
    THUMBNAIL_QUALITY = 95
    THUMBNAIL_FORMAT = 'JPEG'
    THUMBNAIL_PRESERVE_FORMAT = True
    
# 3. Static files compression
WHITENOISE_COMPRESS_OFFLINE = True
WHITENOISE_COMPRESS_OFFLINE_CONTEXT = {
    'static_url': STATIC_URL,
}

# 4. Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'abttech',
        'TIMEOUT': 300,  # 5 minutes
    }
}

# 5. Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'abtapp/media')

# 6. Gzip compression for static files
MIDDLEWARE += [
    'django.middleware.gzip.GZipMiddleware',
    'abtapp.image_optimization.ImageOptimizationMiddleware',
]

# 7. Security headers
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
"""
