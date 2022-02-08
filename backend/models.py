from django.db import models
from django.utils.safestring import mark_safe

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