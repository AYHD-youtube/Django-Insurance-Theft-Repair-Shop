# Generated by Django 4.0.3 on 2022-03-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='is_declined',
            field=models.BooleanField(default=False),
        ),
    ]
