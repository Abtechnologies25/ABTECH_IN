"""
Complete Image Optimization Settings Configuration
Add these settings to your Django settings.py file
"""

import os
from pathlib import Path

# ============================================================================
# IMAGE OPTIMIZATION SETTINGS
# ============================================================================

# 1. PILLOW/PIL Configuration
# ============================================================================

# Image formats allowed for upload
IMAGE_ALLOWED_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'webp']

# Image size limits (in MB)
MAX_IMAGE_SIZE = 10
MAX_THUMBNAIL_SIZE = 5

# SORL Thumbnail Configuration (if using sorl-thumbnail)
THUMBNAIL_DEBUG = False
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'
THUMBNAIL_FORMAT = 'JPEG'
THUMBNAIL_QUALITY = 95  # High quality
THUMBNAIL_PRESERVE_FORMAT = True
THUMBNAIL_ORIENTATION = True
THUMBNAIL_PROGRESSIVE = 100

# Thumbnail aliases for different image sizes
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': 'center'},
        'avatar_large': {'size': (200, 200), 'crop': 'center'},
        'small': {'size': (300, 300), 'crop': 'center'},
        'medium': {'size': (500, 500), 'crop': 'center'},
        'large': {'size': (800, 800), 'crop': 'center'},
        'xlarge': {'size': (1200, 1200), 'crop': 'center'},
        'thumbnail': {'size': (200, 200), 'crop': 'center'},
        'gallery': {'size': (600, 600), 'crop': 'center'},
        'hero': {'size': (1920, 600), 'crop': 'center'},
        'banner': {'size': (1920, 400), 'crop': 'center'},
    }
}

# ============================================================================
# 2. STATIC FILES COMPRESSION
# ============================================================================

# Use WhiteNoise for efficient static file serving
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Enable offline compression
WHITENOISE_COMPRESS_OFFLINE = True
WHITENOISE_COMPRESS_OFFLINE_CONTEXT = {
    'static_url': '/static/',
}

WHITENOISE_MIMETYPES = {
    '.webp': 'image/webp',
}

# ============================================================================
# 3. MIDDLEWARE FOR IMAGE OPTIMIZATION
# ============================================================================

# Add to MIDDLEWARE list in settings.py:
MIDDLEWARE_TO_ADD = [
    'django.middleware.gzip.GZipMiddleware',  # Gzip compression
    'abtapp.image_optimization.ImageOptimizationMiddleware',  # Custom image headers
]

# ============================================================================
# 4. CACHING CONFIGURATION
# ============================================================================

# Redis cache (recommended for production)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'abttech',
        'TIMEOUT': 300,  # 5 minutes
    }
}

# ============================================================================
# 5. IMAGE CACHE HEADERS
# ============================================================================

# Cache control headers (in ImageOptimizationMiddleware)
CACHE_HEADERS = {
    'static_images': 'public, max-age=2592000',  # 30 days
    'media_images': 'public, max-age=604800',    # 7 days
    'thumbnails': 'public, max-age=2592000',     # 30 days
}

# ============================================================================
# 6. MEDIA FILES CONFIGURATION
# ============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'abtapp', 'media')

# ============================================================================
# 7. STATIC FILES CONFIGURATION
# ============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'abtapp', 'static'),
]

# ============================================================================
# 8. DATABASE QUERY OPTIMIZATION
# ============================================================================

# Select related for common image queries
COMMON_SELECT_RELATED = [
    'category',
    'user',
]

COMMON_PREFETCH_RELATED = [
    'images__category',
]

# ============================================================================
# 9. IMAGE PROCESSING OPTIONS
# ============================================================================

# Image processing quality settings
IMAGE_PROCESSING = {
    'QUALITY': {
        'HIGH': 95,      # For thumbnails and gallery
        'MEDIUM': 85,    # For general images
        'LOW': 75,       # For mobile optimization
    },
    'RESIZE': {
        'AUTO_DOWNSIZE': True,
        'MAX_WIDTH': 1920,
        'MAX_HEIGHT': 1080,
    },
    'FORMATS': {
        'SUPPORT_WEBP': True,
        'OPTIMIZE_PNG': True,
        'PROGRESSIVE_JPEG': True,
    }
}

# ============================================================================
# 10. CDN CONFIGURATION (Optional)
# ============================================================================

# If using a CDN like Cloudflare or AWS CloudFront
USE_CDN = False
CDN_URL = os.environ.get('CDN_URL', '')

# Cloudflare specific (if applicable)
CLOUDFLARE_ENABLED = False
CLOUDFLARE_ZONE_ID = os.environ.get('CLOUDFLARE_ZONE_ID', '')
CLOUDFLARE_API_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')

# ============================================================================
# 11. SECURITY SETTINGS FOR IMAGES
# ============================================================================

# File upload restrictions
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Allowed image extensions
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']

# Content Security Policy for images
CSP_IMG_SRC = [
    "'self'",
    'https:',
    'data:',
    '*.cloudflare.com',  # If using Cloudflare
]

# ============================================================================
# 12. PRODUCTION OPTIMIZATION
# ============================================================================

if not DEBUG:
    # Production-specific optimizations
    
    # Enable all security settings
    SECURE_HSTS_SECONDS = 31536000
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Image quality for production (balance between quality and size)
    THUMBNAIL_QUALITY = 90
    
    # Use gzip compression
    MIDDLEWARE = [
        'django.middleware.gzip.GZipMiddleware',
    ] + MIDDLEWARE
    
    # Cache images longer in production
    CACHE_HEADERS = {
        'static_images': 'public, max-age=31536000',  # 1 year
        'media_images': 'public, max-age=2592000',    # 30 days
        'thumbnails': 'public, max-age=31536000',     # 1 year
    }

# ============================================================================
# 13. MONITORING AND LOGGING
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'image_optimization.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'abtapp.image_optimization': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================================================
# 14. QUICK REFERENCE
# ============================================================================

"""
Quick Setup Steps:

1. Install packages:
   pip install Pillow pillow-simd django-imagekit sorl-thumbnail whitenoise

2. Add to INSTALLED_APPS:
   INSTALLED_APPS = [
       ...
       'sorl.thumbnail',
   ]

3. Add to MIDDLEWARE (after SecurityMiddleware):
   MIDDLEWARE = [
       ...
       'django.middleware.gzip.GZipMiddleware',
       'abtapp.image_optimization.ImageOptimizationMiddleware',
       ...
   ]

4. Copy settings from this file to your settings.py

5. Load CSS and JS in base template:
   <link rel="stylesheet" href="{% static 'abtapp/css/image-optimization.css' %}">
   <script src="{% static 'abtapp/js/image-optimization.js' %}"></script>

6. Run migrations and optimize images:
   python manage.py migrate
   python manage.py optimize_images --convert-webp

7. Test with:
   python manage.py runserver
   Visit: https://pagespeed.web.dev

Performance expectations:
- Static images: 200-500ms load time
- Gallery load: 1-2 seconds (all images)
- Page load: 2-3 seconds
- Images: 30-40% of page size (down from 70%)
"""
