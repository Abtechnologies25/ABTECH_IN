from django.test import TestCase
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse


class CareerApplicationTests(TestCase):
    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        EMAIL_HOST='localhost',
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
