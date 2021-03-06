# Generated by Django 4.0.1 on 2022-01-24 13:42

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminauth', '0006_patron_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patron',
            name='payment',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.1'))]),
        ),
        migrations.AlterField(
            model_name='patron',
            name='payment_sum',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.1'))]),
        ),
        migrations.AlterField(
            model_name='patrontostudent',
            name='payed',
            field=models.FloatField(default=0, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.1'))]),
        ),
        migrations.AlterField(
            model_name='student',
            name='contract_sum',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.1'))]),
        ),
        migrations.AlterField(
            model_name='student',
            name='payed_sum',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.1'))]),
        ),
    ]
