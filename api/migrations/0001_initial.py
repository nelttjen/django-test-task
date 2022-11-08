# Generated by Django 4.1.3 on 2022-11-07 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ru_name', models.CharField(max_length=300)),
                ('en_name', models.CharField(max_length=300)),
                ('alt_name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True)),
                ('tags', models.ManyToManyField(related_name='title_tags', to='api.tags')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume_name', models.CharField(max_length=300)),
                ('volume_price', models.IntegerField(default=0)),
                ('volume_number', models.IntegerField()),
                ('volume_title', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='volume_titles', to='api.title')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_number', models.IntegerField()),
                ('chapter_content', models.TextField(blank=True)),
                ('chapter_views_count', models.IntegerField(default=0)),
                ('chapter_likes_count', models.IntegerField(default=0)),
                ('volume', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chapter_volumes', to='api.volume')),
            ],
        ),
    ]
