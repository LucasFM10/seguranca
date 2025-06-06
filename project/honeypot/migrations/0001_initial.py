# Generated by Django 5.2 on 2025-04-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HoneypotLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('ipv4_address', models.GenericIPAddressField()),
                ('post_params', models.JSONField(default=dict)),
            ],
        ),
    ]
