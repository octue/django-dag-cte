# Generated by Django 2.2.9 on 2020-02-08 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('node_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('parents', models.ManyToManyField(related_name='children', to='tests.Node')),
            ],
        ),
    ]
