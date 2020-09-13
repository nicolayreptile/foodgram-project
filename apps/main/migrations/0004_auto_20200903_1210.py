# Generated by Django 3.1 on 2020-09-03 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200903_1205'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeIngridients',
            new_name='RecipeIngredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.CreateModel(
            name='RecipeTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='main.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='main.tag')),
            ],
        ),
    ]
