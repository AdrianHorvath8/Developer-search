# Generated by Django 4.0.2 on 2022-07-02 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_message_options_alter_profile_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-name']},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='created',
        ),
    ]