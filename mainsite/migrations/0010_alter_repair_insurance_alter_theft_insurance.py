# Generated by Django 4.0.3 on 2022-03-20 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0009_remove_insurance_claim_type_remove_repair_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='insurance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.insurance'),
        ),
        migrations.AlterField(
            model_name='theft',
            name='insurance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.insurance'),
        ),
    ]
