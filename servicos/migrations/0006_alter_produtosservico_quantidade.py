# Generated by Django 5.2 on 2025-05-13 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0005_alter_servico_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtosservico',
            name='quantidade',
            field=models.DecimalField(decimal_places=2, default=1.0, help_text='Quantidade utilizada de produto', max_digits=5, verbose_name='Quantidade'),
        ),
    ]
