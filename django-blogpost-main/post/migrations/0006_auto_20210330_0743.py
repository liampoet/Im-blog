# Generated by Django 3.1.7 on 2021-03-30 07:43

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20210330_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=post.models.post_image_path),
        ),
    ]
