from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.utils.html import format_html

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 5  # Number of empty forms you want to show

class GalleryCategoryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]


class VideoAdmin(admin.ModelAdmin):
    list_display = ("CODE", "UPLOADED_DATE", "TITLE", "TYPE", "YOUTUBE_LINK", "video_preview")
    search_fields = ("TITLE", "CODE")
    list_filter = ("TITLE",)

    def video_preview(self, obj):
        return format_html(
            '<iframe width="200" height="120" src="{}" frameborder="0" allowfullscreen></iframe>',
            obj.embed_link(),
        )
    video_preview.short_description = "Preview"


class MoUAdmin(admin.ModelAdmin):
    list_display = ('MoU_NO', 'ORGANIZATION_NAME', 'LOCATION', 'OFFICIAL_WEBSITE', 'DATE_OF_MoU', 'VALIDITY')
    search_fields = ('MoU_NO', 'ORGANIZATION_NAME', 'LOCATION')
    list_filter = ('DATE_OF_MoU', 'VALIDITY')

admin.site.register(Video, VideoAdmin)
admin.site.register(MoU, MoUAdmin)
admin.site.register(GalleryCategory, GalleryCategoryAdmin)
admin.site.register(GalleryImage)
