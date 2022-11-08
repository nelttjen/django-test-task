from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin

from .models import Title, Tags, Volume, Chapter


class TagInline(admin.TabularInline):
    model = Title.tags.through


class VolumeInline(admin.TabularInline):
    model = Volume


class ChapterInline(admin.StackedInline):
    model = Chapter


class TitleAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'en_name', 'ru_name')
    list_display_links = ('id', 'en_name')
    search_fields = ('ru_name', 'en_name', 'alt_name')
    search_help_text = f'Search by: {", ".join(search_fields)}'
    exclude = ('tags',)

    inlines = [TagInline, VolumeInline, ]


class VolumeAdmin(admin.ModelAdmin):
    ordering = ('-id', )
    list_display = ('id', 'volume_number', 'volume_name', 'volume_price', 'volume_title')
    list_display_links = ('id', 'volume_number', 'volume_name')
    search_fields = ('volume_name', 'volume_title__en_name', 'volume_title__ru_name', 'volume_title__alt_name')
    search_help_text = f'Search by: {", ".join(search_fields)}'

    inlines = [ChapterInline, ]


class ChapterAdmin(admin.ModelAdmin):
    ordering = ('-id', )
    list_display = ('id', 'chapter_number', 'chapter_views_count', 'chapter_likes_count', 'volume')
    list_display_links = ('id', 'chapter_number', 'chapter_views_count', 'chapter_likes_count')
    search_fields = ('id', 'volume__volume_name')
    search_help_text = f'Search by: {", ".join(search_fields)}'


class TagsAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = search_fields = ('id', 'tag_name')
    list_editable = ('tag_name', )
    search_help_text = f'Search by: {", ".join(search_fields)}'


admin.site.register(Title, TitleAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Tags, TagsAdmin)