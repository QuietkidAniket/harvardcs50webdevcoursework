# Generated by Django 4.0.5 on 2022-07-05 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(max_length=500)),
                ('startingBid', models.FloatField()),
                ('currentBid', models.FloatField(blank=True, null=True)),
                ('flactive', models.BooleanField(default=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_listings', to='auctions.category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creators_list', to=settings.AUTH_USER_MODEL)),
                ('spectators', models.ManyToManyField(blank=True, related_name='spectators_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('creationdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]