from django.contrib import admin


from .models import Title, Tags, Volume, Chapter


# Register your models here.
class TitleAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'ru_name', 'en_name')
    list_display_links = ('id', 'ru_name')
    search_fields = ('ru_name', 'en_name', 'alt_name')


admin.site.register(Title, TitleAdmin)
admin.site.register(Tags)
admin.site.register(Volume)
admin.site.register(Chapter)