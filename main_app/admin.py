from django.contrib import admin

from main_app.models import Assets, Files, Events


# Register your models here.
@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    pass





@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    pass


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    pass