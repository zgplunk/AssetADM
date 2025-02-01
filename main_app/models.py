import uuid

from django.db import models
import datetime


# Create your models here.
class Assets(models.Model):
    def __str__(self):
        return self.Na

    No = models.CharField(max_length=50, verbose_name='编号', null=True, blank=True)
    Na = models.CharField(max_length=50, verbose_name='名称', null=True, blank=True)
    Mo = models.CharField(max_length=50, verbose_name='规格/型号', null=True, blank=True)
    Co = models.IntegerField(verbose_name='数量', null=True, blank=True)
    Ma = models.CharField(max_length=50, verbose_name='生产厂家', null=True, blank=True)
    Ra = models.CharField(max_length=50, verbose_name='量程', null=True, blank=True)
    Lo = models.CharField(max_length=50, verbose_name='存放货架', null=True, blank=True)
    St = models.BooleanField(verbose_name='借出状态', null=True, blank=True)
    Bo = models.DateField(auto_now=False, verbose_name='借出时间', null=True, blank=True)
    Ba = models.DateField(auto_now=False, verbose_name='预计归还时间', null=True, blank=True)
    Po = models.CharField(max_length=50, verbose_name='借用项目', null=True, blank=True)
    Rm = models.TextField(verbose_name='备注', null=True, blank=True)


class Events(models.Model):
    Msd_event_Choise = (
        ('借出', '借出'),
        ('归还', '归还'),
        ('删除', '删除'),
        ('归档', '归档'),
        ('新建', '新建')
    )

    def __str__(self):
        return f"{self.context}"

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    context = models.TextField(default=None, null=True, blank=True)


class Files(models.Model):
    def __str__(self):
        return self.Ti.name

    Ti = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name='文件名')
    Dt = models.DateTimeField(auto_created=True, verbose_name='上传时间')
    As = models.ForeignKey(Assets, on_delete=models.CASCADE, verbose_name='资产')


class Tables(models.Model):
    St_Outgoing_Choise = (
        ('进行', '进行'),
        ('结束', '结束'),
        ('挂起', '挂起')
    )

    def __str__(self):
        return str(self.Name_person) + '的' + str(self.Project) + '项目'

    Number_form = models.CharField(max_length=50, verbose_name='出库单编号', null=True, blank=True)
    Name_person = models.CharField(max_length=50, verbose_name='负责人', null=True, blank=True)
    Create_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间', null=True, blank=True)
    Start_date = models.DateField(verbose_name='出库时间', null=True, blank=True, auto_now=False)
    End_date = models.DateField(verbose_name='预计入库时间', null=True, blank=True, auto_now=False)
    Project = models.CharField(max_length=50, verbose_name='申请项目', null=True, blank=True)
    Status = models.CharField(max_length=10, verbose_name='单状态', null=True, blank=True, choices=St_Outgoing_Choise)
    Form_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Asset_list = models.TextField(verbose_name='归档设备列表', null=True, blank=True, default='')


class RecordTables(models.Model):
    def __str__(self):
        return f"{self.Table}的记录"

    Table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    Asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    DateTime = models.DateTimeField(auto_now_add=True)
    IdentfyCode = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
