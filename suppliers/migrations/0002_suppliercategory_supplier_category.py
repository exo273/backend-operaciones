# Generated migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Categoría de Proveedor',
                'verbose_name_plural': 'Categorías de Proveedores',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='supplier',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppliers', to='suppliers.suppliercategory', verbose_name='Categoría'),
        ),
        migrations.AddIndex(
            model_name='supplier',
            index=models.Index(fields=['category'], name='suppliers_s_categor_e5c6e9_idx'),
        ),
    ]
