# Generated by Django 2.2.12 on 2020-08-16 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userIpdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30)),
                ('ip_address', models.GenericIPAddressField()),
                ('with_mask_count', models.IntegerField()),
                ('without_mask_count', models.IntegerField()),
            ],
            options={
                'db_table': 'User_IPDetails',
            },
        ),
    ]
