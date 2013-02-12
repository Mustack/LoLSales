from django.db.models.query import EmptyQuerySet
from django.core.management.base import BaseCommand, CommandError
from notifications.models import Notification
from champions.models import Sale
from accounts.models import Subscription
from datetime import date
from collections import defaultdict

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Notify subscribed users about sales'

    def handle(self, *args, **options):
        today = date.today()

        to_notify = EmptyQuerySet()

        # Iterate over sales that are in effect
        for sale in Sale.objects.filter(start__lte=today,
                                            end__gte=today):
            # Find subscriptions that require the products on sale
            subscriptions = Subscription.objects.filter(product__in=sale.products.all())

            # Remove subscriptions that have been notified
            subscriptions = subscriptions.exclude(notifications__sale=sale)

            to_notify |= subscriptions

        # Collect the subscriptions by user
        user_subs = defaultdict(list)
        for sub in to_notify:
            user_subs[sub.user].append(sub)

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@example.com')

        # Build the emails
        for user, subs in user_subs.iteritems():
            to_email = user.email

            context = {'user': user, 'subscriptions': subs}

            subject = render_to_string('notifications/sale_subject.txt', context).replace('\n', '').strip()

            context['subject'] = subject

            text_content = render_to_string('notifications/sale_body.txt', context)
            html_content = render_to_string('notifications/sale_body.html', context)

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, 'text/html')

            msg.send() # Will raise exceptions on failure

            # Mark all active sales for this product as notified
            for sub in subs:
                for sale in sub.product.active_sales.all():
                    notified = Notification()
                    notified.sale = sale
                    notified.subscription = sub
                    notified.save()
