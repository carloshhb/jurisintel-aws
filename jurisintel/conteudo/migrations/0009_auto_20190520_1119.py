# Generated by Django 2.1.7 on 2019-05-20 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0008_auto_20190520_1119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tema',
            old_name='ementa',
            new_name='ementas',
        ),
        migrations.AlterField(
            model_name='tema',
            name='identifier_code',
            field=models.CharField(default='e8f39c2bf812d5ac', max_length=150, unique=True),
        ),
    ]
