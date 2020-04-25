# Generated by Django 3.0.5 on 2020-04-25 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=35)),
                ('dPaid', models.DateField()),
                ('dSent', models.DateField()),
                ('dViewed', models.DateField()),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Client')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('default_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Company')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('amount', models.IntegerField()),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Invoice')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('vat', models.CharField(max_length=200)),
                ('commerce', models.CharField(max_length=200)),
                ('logo', models.IntegerField()),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Company')),
            ],
        ),
        migrations.CreateModel(
            name='ClientDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('logo', models.IntegerField()),
                ('vat', models.CharField(max_length=200)),
                ('commerce', models.CharField(max_length=200)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Client')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Company'),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('iban', models.CharField(max_length=34)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Company')),
                ('currency_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Currency')),
            ],
        ),
    ]