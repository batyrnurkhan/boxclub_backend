# Generated by Django 5.0.4 on 2024-12-03 06:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProbableFight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_name', models.CharField(max_length=255)),
                ('weight_category', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fighter1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter1_fights', to=settings.AUTH_USER_MODEL)),
                ('fighter2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter2_fights', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
