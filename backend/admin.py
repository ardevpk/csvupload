from distutils.command.upload import upload
from django.contrib import admin
from .models import uploader
# Register your models here.
class uploadPage(admin.ModelAdmin):
    # list_disply = ['file']
    readonly_fields = ('file', )


admin.site.register(uploader, uploadPage)