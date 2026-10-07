from django.test import TestCase
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse


class RobotsTxtTests(TestCase):
    def test_robots_txt_is_served_as_plain_text(self):
        response = self.client.get(reverse('robots_txt'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'User-agent: *')
        self.assertContains(response, 'Allow: /')
        self.assertContains(response, 'Disallow: /admin/')
        self.assertContains(response, 'Sitemap: http://testserver/sitemap.xml')


class SitemapTests(TestCase):
    def test_sitemap_is_generated_from_python(self):
        response = self.client.get(reverse('sitemap'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertContains(response, '<loc>http://testserver/</loc>')
        self.assertContains(response, '<loc>http://testserver/projects/</loc>')
        self.assertNotContains(response, '<lastmod>')

    def test_project_category_pages_are_included(self):
        from .models import ProjectCategory

        category = ProjectCategory.objects.create(name='Sitemap Test Category')

        response = self.client.get(reverse('sitemap'))

        self.assertContains(
            response,
            f'<loc>http://testserver/projects/{category.pk}/</loc>',
        )


class CareerApplicationTests(TestCase):
    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        EMAIL_HOST='smtp.gmail.com',
        EMAIL_HOST_USER='abtech.mgmt@gmail.com',
        EMAIL_HOST_PASSWORD='test-app-password',
        DEFAULT_FROM_EMAIL='careers@example.com',
    )
    def test_application_emails_resume_to_career_inbox(self):
        resume = SimpleUploadedFile('resume.pdf', b'%PDF-1.4 sample')

        response = self.client.post(
            reverse('career'),
            {
                'full_name': 'Applicant Name',
                'email': 'applicant@example.com',
                'phone': '9876543210',
                'resume': resume,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['abtechchennai@gmail.com'])
        self.assertEqual(mail.outbox[0].from_email, 'careers@example.com')
        self.assertEqual(mail.outbox[0].reply_to, ['applicant@example.com'])
        self.assertEqual(mail.outbox[0].attachments[0][0], 'resume.pdf')

    def test_application_rejects_invalid_phone_number(self):
        resume = SimpleUploadedFile('resume.pdf', b'%PDF-1.4 sample')

        response = self.client.post(
            reverse('career'),
            {
                'full_name': 'Applicant Name',
                'email': 'applicant@example.com',
                'phone': '123',
                'resume': resume,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])
