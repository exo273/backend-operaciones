# Generated manually

from django.db import migrations, models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='waste_percentage',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Porcentaje de merma o desperdicio del producto (0-100%)',
                max_digits=5,
                null=True,
                validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))],
                verbose_name='Porcentaje de Merma'
            ),
        ),
    ]
