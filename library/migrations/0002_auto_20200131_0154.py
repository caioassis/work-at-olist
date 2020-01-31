# Generated by Django 2.2.9 on 2020-01-31 01:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('edition', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Edition')),
                ('publication_year', models.PositiveIntegerField(verbose_name='Publication Year')),
                ('authors', models.ManyToManyField(related_name='books', to='library.Author', verbose_name='Authors')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['name'], name='idx_book_name'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['publication_year'], name='idx_book_publication_year'),
        ),
    ]