from django.core.management.base import BaseCommand
from datetime import date
from abtapp.models import Video, Video2


class Command(BaseCommand):
    help = 'Populate sample videos for Channel 1 and Channel 2'

    def handle(self, *args, **options):
        # Channel 1 Videos
        channel1_videos = [
            {
                'CODE': 'VID-CH1-001',
                'TITLE': 'IoT Basics Tutorial',
                'TYPE': 'BASICS',
                'YOUTUBE_LINK': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'UPLOADED_DATE': date(2024, 10, 1)
            },
            {
                'CODE': 'VID-CH1-002',
                'TITLE': 'Smart Home Project Demo',
                'TYPE': 'PROJECTS',
                'YOUTUBE_LINK': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'UPLOADED_DATE': date(2024, 10, 5)
            },
            {
                'CODE': 'VID-CH1-003',
                'TITLE': 'Embedded Systems Workshop',
                'TYPE': 'PRODUCTS',
                'YOUTUBE_LINK': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'UPLOADED_DATE': date(2024, 10, 10)
            }
        ]

        # Add Channel 1 Videos
        for video_data in channel1_videos:
            video, created = Video.objects.get_or_create(
                CODE=video_data['CODE'],
                defaults=video_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Channel 1: {video.CODE} - {video.TITLE}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {video.CODE}"))

        self.stdout.write(self.style.SUCCESS(f"\nChannel 1 Total: {Video.objects.count()} videos"))
        self.stdout.write(self.style.SUCCESS(f"Channel 2 Total: {Video2.objects.count()} videos"))
