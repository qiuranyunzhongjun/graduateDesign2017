# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FuncData',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('point_no', models.PositiveSmallIntegerField(verbose_name='所测量的位置编号')),
                ('measure_func_data', models.FloatField(verbose_name='功能数据')),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('eye_choice', models.CharField(choices=[('L', 'left eye'), ('R', 'right eye')], verbose_name='左眼or右眼', default='R', max_length=1)),
                ('measure_date', models.DateField(verbose_name='测试日期')),
                ('owner', models.ForeignKey(related_name='measures', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('firstname', models.IntegerField(serialize=False, verbose_name='匿名化ID', primary_key=True)),
                ('register_date', models.DateField(verbose_name='录入时间')),
                ('owner', models.ForeignKey(related_name='patients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('firstname',),
            },
        ),
        migrations.CreateModel(
            name='StruData',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('area_no', models.PositiveSmallIntegerField(verbose_name='所测量的区域编号')),
                ('avg_data', models.FloatField(verbose_name='结构数据')),
                ('measure', models.ForeignKey(to='analyses.Measure')),
            ],
        ),
        migrations.AddField(
            model_name='measure',
            name='patient',
            field=models.ForeignKey(to='analyses.Patient'),
        ),
        migrations.AddField(
            model_name='funcdata',
            name='measure',
            field=models.ForeignKey(to='analyses.Measure'),
        ),
    ]
