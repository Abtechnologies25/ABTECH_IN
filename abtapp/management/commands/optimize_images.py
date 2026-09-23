"""
Django Management Command: Optimize Images
Compresses and converts images to WebP format for better performance

Usage:
    python manage.py optimize_images
    python manage.py optimize_images --quality 85
    python manage.py optimize_images --convert-webp
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Optimize images in static and media directories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality',
            type=int,
            default=95,
            help='JPEG quality (1-100, default: 95)'
        )
        parser.add_argument(
            '--convert-webp',
            action='store_true',
            help='Convert PNG/JPEG to WebP format'
        )
        parser.add_argument(
            '--optimize-size',
            action='store_true',
            help='Resize large images to standard sizes'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without applying them'
        )

    def handle(self, *args, **options):
        quality = options['quality']
        convert_webp = options['convert_webp']
        optimize_size = options['optimize_size']
        dry_run = options['dry_run']

        self.stdout.write(self.style.SUCCESS('🚀 Starting Image Optimization...'))
        self.stdout.write(f'Quality: {quality}%')
        self.stdout.write(f'Convert to WebP: {convert_webp}')
        self.stdout.write(f'Optimize Size: {optimize_size}')
        self.stdout.write(f'Dry Run: {dry_run}\n')

        # Optimize static images
        static_dir = os.path.join(settings.BASE_DIR, 'abtapp', 'static', 'abtapp', 'images')
        self.optimize_directory(static_dir, quality, convert_webp, optimize_size, dry_run)

        # Optimize media images
        media_dir = os.path.join(settings.BASE_DIR, 'abtapp', 'media')
        self.optimize_directory(media_dir, quality, convert_webp, optimize_size, dry_run)

        self.stdout.write(self.style.SUCCESS('\n✅ Image optimization complete!'))

    def optimize_directory(self, directory, quality, convert_webp, optimize_size, dry_run):
        """Optimize all images in a directory"""
        if not os.path.exists(directory):
            self.stdout.write(self.style.WARNING(f'Directory not found: {directory}'))
            return

        supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        image_files = []

        # Recursively find all image files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(supported_formats):
                    image_files.append(os.path.join(root, file))

        self.stdout.write(f'Found {len(image_files)} images in {directory}')

        for image_path in image_files:
            try:
                self.optimize_image(
                    image_path,
                    quality,
                    convert_webp,
                    optimize_size,
                    dry_run
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {image_path}: {str(e)}')
                )

    def optimize_image(self, image_path, quality, convert_webp, optimize_size, dry_run):
        """Optimize a single image"""
        try:
            # Get file info
            original_size = os.path.getsize(image_path)
            
            # Open image
            img = Image.open(image_path)
            
            # Get image info
            width, height = img.size
            format_name = img.format
            
            # Optimize based on options
            if optimize_size:
                img = self.resize_image_if_needed(img)
            
            # Convert mode if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                if format_name != 'PNG':
                    img = img.convert('RGB')
            
            # Save optimized version
            if not dry_run:
                save_kwargs = {
                    'quality': quality,
                    'optimize': True,
                }
                
                # Save original format
                img.save(image_path, format_name or 'JPEG', **save_kwargs)
                
                # Save WebP version if requested
                if convert_webp and format_name in ('JPEG', 'PNG', 'JPG'):
                    webp_path = image_path.rsplit('.', 1)[0] + '.webp'
                    img.save(webp_path, 'WEBP', quality=quality)
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created WebP: {os.path.basename(webp_path)}')
                    )
            
            new_size = os.path.getsize(image_path) if os.path.exists(image_path) else original_size
            saved_percent = ((original_size - new_size) / original_size * 100) if original_size > 0 else 0
            
            status = '[DRY RUN] ' if dry_run else ''
            self.stdout.write(
                f'{status}✓ {os.path.basename(image_path)} '
                f'({width}x{height}) - '
                f'Saved {saved_percent:.1f}% '
                f'({self.format_bytes(original_size)} → {self.format_bytes(new_size)})'
            )

        except Exception as e:
            logger.error(f'Error optimizing {image_path}: {str(e)}')
            raise

    def resize_image_if_needed(self, img):
        """Resize image if it exceeds standard sizes"""
        max_width = 1920
        max_height = 1080
        
        width, height = img.size
        
        if width > max_width or height > max_height:
            # Calculate aspect ratio
            aspect_ratio = width / height
            
            if aspect_ratio > max_width / max_height:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
            
            img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
        
        return img

    @staticmethod
    def format_bytes(bytes_value):
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB']:
            if bytes_value < 1024.0:
                return f'{bytes_value:.1f}{unit}'
            bytes_value /= 1024.0
        return f'{bytes_value:.1f}GB'
