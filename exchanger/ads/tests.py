from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ads.models import Ad, ExchangeProposal


class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Телефон',
            description='Почти новый',
            category='Электроника',
            condition='б/у',
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.title, 'Телефон')
        self.assertIsNotNone(self.ad.created_at)
        self.assertEqual(str(self.ad), self.ad.title)


class ExchangeProposalModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.ad1 = Ad.objects.create(user=self.user1, title='Товар 1', description='...', category='Книги', condition='новый')
        self.ad2 = Ad.objects.create(user=self.user2, title='Товар 2', description='...', category='Одежда', condition='б/у')

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Поменяемся?',
            status='pending'
        )

    def test_proposal_creation(self):
        self.assertEqual(self.proposal.status, 'pending')
        self.assertEqual(self.proposal.ad_sender.title, 'Товар 1')


class AdViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_ad(self):
        response = self.client.post(reverse('ad_create'), {
            'title': 'Ноутбук',
            'description': 'Рабочий ноут',
            'category': 'electronics',
            'condition': 'new',
            'image_url': 'http://example.com/image.jpg',
        })
        print('Status:', response.status_code)
        print('Errors (if any):', response.context['form'].errors if response.context else 'No form')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='Ноутбук').exists())

    def test_edit_ad_by_author(self):
        ad = Ad.objects.create(
            user=self.user,
            title='Старое название',
            description='desc',
            category='sport',
            condition='used',
        )
        response = self.client.post(reverse('ad_edit', args=[ad.id]), {
            'title': 'Новое название',
            'description': ad.description,
            'category': ad.category,
            'condition': ad.condition,
        })
        ad.refresh_from_db()
        self.assertEqual(ad.title, 'Новое название')

    def test_delete_ad_by_author(self):
        ad = Ad.objects.create(user=self.user, title='Удалить', description='desc', category='Спорт', condition='used')
        response = self.client.post(reverse('ad_delete', args=[ad.id]), follow=True)
        self.assertFalse(Ad.objects.filter(pk=ad.pk).exists())
        self.assertEqual(response.status_code, 200)


class ExchangeProposalViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

        self.ad_sender = Ad.objects.create(user=self.sender, title='Sender Ad', description='...', category='Разное', condition='б/у')
        self.ad_receiver = Ad.objects.create(user=self.receiver, title='Receiver Ad', description='...', category='Разное', condition='новый')

    def test_create_proposal(self):
        self.client.login(username='sender', password='pass')
        url = reverse('propose_exchange', args=[self.ad_receiver.id])
        response = self.client.post(url, {
            'ad_sender': self.ad_sender.id,
            'ad_receiver': self.ad_receiver.id,
            'comment': 'Обмен?',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_accept_proposal(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad_sender, ad_receiver=self.ad_receiver, comment='?', status='pending')
        self.client.login(username='receiver', password='pass')
        url = reverse('accept_proposal', args=[proposal.id])
        response = self.client.post(url)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')

    def test_reject_proposal(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad_sender, ad_receiver=self.ad_receiver, comment='?', status='pending')
        self.client.login(username='receiver', password='pass')
        url = reverse('reject_proposal', args=[proposal.id])
        response = self.client.post(url)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'rejected')


class ProposalFilteringTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_a = User.objects.create_user(username='a', password='pass')
        self.user_b = User.objects.create_user(username='b', password='pass')

        self.ad_a1 = Ad.objects.create(user=self.user_a, title='Ad A1', description='...', category='Электроника', condition='новый')
        self.ad_b1 = Ad.objects.create(user=self.user_b, title='Ad B1', description='...', category='Одежда', condition='б/у')

        self.proposal1 = ExchangeProposal.objects.create(ad_sender=self.ad_a1, ad_receiver=self.ad_b1, status='pending')
        self.proposal2 = ExchangeProposal.objects.create(ad_sender=self.ad_a1, ad_receiver=self.ad_b1, status='accepted')

    def test_filter_by_status(self):
        self.client.login(username='b', password='pass')
        response = self.client.get(reverse('incoming') + '?status=accepted')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'accepted')

    def test_filter_by_sender(self):
        self.client.login(username='b', password='pass')
        response = self.client.get(reverse('incoming') + '?sender=a')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad A1')

    def test_filter_by_receiver(self):
        self.client.login(username='a', password='pass')
        response = self.client.get(reverse('outgoing') + '?receiver=b')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad B1')
