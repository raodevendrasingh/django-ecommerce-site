# Generated by Django 4.2.6 on 2024-01-20 17:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingdetails',
            old_name='address',
            new_name='address_level_1',
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='address_level_2',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='country',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
