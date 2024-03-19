# Generated by Django 4.2.6 on 2024-03-19 11:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_tag_product_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]