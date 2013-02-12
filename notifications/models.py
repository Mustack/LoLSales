from django.db import models
from accounts.models import Subscription
from champions.models import Sale

class Notification(models.Model):
    '''Represents a notification sent to a user about a particular sale'''
    subscription = models.ForeignKey(Subscription, related_name='notifications')
    sale = models.ForeignKey(Sale, related_name='notifications')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{} -> {} ({})'.format(self.subscription.user.username,
                                    self.subscription.product.name,
                                    self.sale.name)
