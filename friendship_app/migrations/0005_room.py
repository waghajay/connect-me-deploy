# Generated by Django 5.0.3 on 2024-04-04 20:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_userprofile_online_status'),
        ('friendship_app', '0004_friendship_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(default='', max_length=100)),
                ('user1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_user_1', to='authentication.userprofile')),
                ('user2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_user_2', to='authentication.userprofile')),
            ],
        ),
    ]
