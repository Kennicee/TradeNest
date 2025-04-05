# Generated by Django 5.2 on 2025-04-05 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_alter_product_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='default_category', max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Default Product', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
    ]
