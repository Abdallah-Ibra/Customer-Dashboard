# Generated by Django 3.2.5 on 2021-07-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_auto_20210728_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(to='bookstore.Tag'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('In Progress', 'In Progress'), ('Out Progress', 'Out Progress')], max_length=200, null=True),
        ),
    ]
