# Generated by Django 4.2.6 on 2023-11-27 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_fname_customer_name_remove_customer_lname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]