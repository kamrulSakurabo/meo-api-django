# Generated by Django 4.2.1 on 2023-06-02 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_shop', '0002_rankingpalace_category_rankingpalace_cid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankingsearch',
            name='search_data',
            field=models.DateField(auto_now_add=True),
        ),
    ]
