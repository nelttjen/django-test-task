from django.db import models


# Create your models here.
class Title(models.Model):
    ru_name = models.CharField(max_length=300)
    en_name = models.CharField(max_length=300)
    alt_name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('Tags', related_name='title_tags')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'Title id {self.id}: {self.en_name} ({self.ru_name})'


class Volume(models.Model):
    volume_title = models.ForeignKey('Title', on_delete=models.PROTECT, related_name='volume_titles')
    volume_name = models.CharField(max_length=300)
    volume_price = models.IntegerField(default=0)
    volume_number = models.IntegerField()


class Chapter(models.Model):
    volume = models.ForeignKey('Volume', on_delete=models.PROTECT, related_name='volume_chapters')
    chapter_number = models.IntegerField()
    chapter_content = models.TextField(blank=True)

    chapter_views_count = models.IntegerField(default=0)
    chapter_likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-id', )


class Tags(models.Model):
    tag_name = models.CharField(max_length=300)

    def __str__(self):
        return self.tag_name

