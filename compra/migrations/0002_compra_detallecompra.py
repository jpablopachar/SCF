# Generated by Django 2.2.6 on 2020-02-17 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_auto_20200214_1837'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compra', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('usuarioModifica', models.IntegerField(blank=True, null=True)),
                ('fechaCompra', models.DateField(blank=True, null=True)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('numFactura', models.CharField(max_length=100)),
                ('fechaFactura', models.DateField()),
                ('subTotal', models.FloatField(default=0)),
                ('descuento', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compra.Proveedor')),
                ('usuarioCrea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
            },
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('usuarioModifica', models.IntegerField(blank=True, null=True)),
                ('cantidad', models.BigIntegerField(default=0)),
                ('precio', models.FloatField(default=0)),
                ('subTotal', models.FloatField(default=0)),
                ('descuento', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('costo', models.FloatField(default=0)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compra.Compra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto')),
                ('usuarioCrea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle compra',
                'verbose_name_plural': 'Detalle compras',
            },
        ),
    ]
