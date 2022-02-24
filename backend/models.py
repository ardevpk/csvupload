from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

# Create your models here.
class uploader(models.Model):
    username = models.CharField(max_length=256)
    file = models.FileField(upload_to='')
    
    def __str__(self):
        return self.username

    def fieldname_download(self):
        return mark_safe('<a href="/media/{0}" download>{1}</a>'.format(
        self.file, self.file))
    file.short_description = 'Download Fieldname'


class Paid(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class StripeOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, default='Pending')