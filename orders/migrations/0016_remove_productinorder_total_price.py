# Generated by Django 3.1.3 on 2020-11-25 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_productinorder_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinorder',
            name='total_price',
        ),
    ]