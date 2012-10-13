# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import a1lite_settings

class Payment(models.Model):

    STATUS_PAY_WAITING = 1
    STATUS_PARTIALLY_PAID = 2
    STATUS_CANCELED = 3
    STATUS_EXPIRED = 4
    STATUS_PAYED = 5

    STATUS_CHOICES = (
        (STATUS_PAY_WAITING, _('Pay waiting')),
        (STATUS_CANCELED, _('Canceled')),
        (STATUS_EXPIRED, _('Expired')),
        (STATUS_PARTIALLY_PAID, _('Partially paid')),
        (STATUS_PAYED, _('Payed')),
    )

    user = models.ForeignKey(User, verbose_name=_('User'))
    status = models.PositiveSmallIntegerField(verbose_name=_('Status'),
        choices=STATUS_CHOICES, default=STATUS_PAY_WAITING)

    cost = models.PositiveIntegerField(verbose_name=_('Cost'))

    default_email = models.EmailField(verbose_name=_('Email'),
        null=True, blank=True)
    phone_number = models.CharField(verbose_name=_('Phone number'),
        max_length=32, null=True, blank=True)

    name = models.CharField(verbose_name=_('Name'),
        help_text=_('Name of product or service'),
        max_length=128, null=True, blank=True)
    comment = models.CharField(verbose_name=_('Comment'),
        help_text=_('Payment comment'),
        max_length=512, null=True, blank=True)

    tid = models.PositiveIntegerField(verbose_name=_('Transaction ID'),
        null=True, blank=True)
    payment_type = models.ForeignKey('PaymentType', verbose_name=_('Payment type'),
        null=True, blank=True)

    partner_income = models.PositiveIntegerField(verbose_name=_('Partner income'),
        null=True, blank=True)
    system_income = models.PositiveIntegerField(verbose_name=_('System income'),
        null=True, blank=True)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta():
        verbose_name=_('Payment')
        verbose_name_plural=_('Payments')

    def __unicode__(self):
        return '%d (%d) / %s' % (self.id, self.cost, unicode(self.status_verbose))

    @property
    def status_verbose(self):
        return [ x[1] for x in self.STATUS_CHOICES
                               if x[0] == self.status ][0]

    def is_payed(self):
        return self.status == self.STATUS_PAYED

class PaymentType(models.Model):
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=512)
    logo = models.ImageField(null=True, blank=True,
        upload_to=a1lite_settings.A1LITE_PAYMENT_TYPE_LOGO_UPLOAD_TO)

    class Meta():
        verbose_name=_('Payment type')
        verbose_name_plural=_('Payment types')

    def __unicode__(self):
        return self.title
