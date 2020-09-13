# Generated by Django 3.1 on 2020-09-03 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20200903_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='recipes', to='main.Tag'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_recipes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='RecipeTags',
        ),
    ]
