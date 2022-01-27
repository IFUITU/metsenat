# Generated by Django 4.0.1 on 2022-01-26 23:55

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminauth', '0008_alter_patron_payment_alter_patron_payment_sum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patron',
            name='payment',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='patron',
            name='payment_sum',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='student',
            name='contract_sum',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='student',
            name='payed_sum',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
