# Generated by Django 4.0.4 on 2022-05-26 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomadmin', '0001_initial'),
        ('ecomapp', '0015_product_sold_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sold_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecomadmin.admin'),
        ),
    ]
