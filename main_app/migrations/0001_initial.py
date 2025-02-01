# Generated by Django 5.1.1 on 2025-01-15 06:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('No', models.CharField(blank=True, max_length=50, null=True, verbose_name='编号')),
                ('Na', models.CharField(blank=True, max_length=50, null=True, verbose_name='名称')),
                ('Mo', models.CharField(blank=True, max_length=50, null=True, verbose_name='规格/型号')),
                ('Co', models.IntegerField(blank=True, null=True, verbose_name='数量')),
                ('Ma', models.CharField(blank=True, max_length=50, null=True, verbose_name='生产厂家')),
                ('Ra', models.CharField(blank=True, max_length=50, null=True, verbose_name='量程')),
                ('Lo', models.CharField(blank=True, max_length=50, null=True, verbose_name='存放货架')),
                ('St', models.BooleanField(blank=True, null=True, verbose_name='借出状态')),
                ('Bo', models.DateField(blank=True, null=True, verbose_name='借出时间')),
                ('Ba', models.DateField(blank=True, null=True, verbose_name='预计归还时间')),
                ('Po', models.CharField(blank=True, max_length=50, null=True, verbose_name='借用项目')),
                ('Rm', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('context', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number_form', models.CharField(blank=True, max_length=50, null=True, verbose_name='出库单编号')),
                ('Name_person', models.CharField(blank=True, max_length=50, null=True, verbose_name='负责人')),
                ('Create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='申请时间')),
                ('Start_date', models.DateField(blank=True, null=True, verbose_name='出库时间')),
                ('End_date', models.DateField(blank=True, null=True, verbose_name='预计入库时间')),
                ('Project', models.CharField(blank=True, max_length=50, null=True, verbose_name='申请项目')),
                ('Status', models.CharField(blank=True, choices=[('进行', '进行'), ('结束', '结束'), ('挂起', '挂起')], max_length=10, null=True, verbose_name='单状态')),
                ('Form_uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Asset_list', models.TextField(blank=True, default='', null=True, verbose_name='归档设备列表')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dt', models.DateTimeField(auto_created=True, verbose_name='上传时间')),
                ('Ti', models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name='文件名')),
                ('As', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.assets', verbose_name='资产')),
            ],
        ),
    ]
