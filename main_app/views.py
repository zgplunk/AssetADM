import os
from uuid import uuid4
from django.urls import reverse as rvs
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from main_app.models import *
from django.views.decorators.csrf import csrf_exempt
import datetime
from spire.barcode import *
import qrcode


# Create your views here.

'''本站域名'''
root_url = "http://localhost:8000/assetsmanagermini/home/"

'''
    备忘录：
    目前二维码是实时生成的，
    但是未来希望再做一次盘点，重新盘点时希望为所有的设备进行拍照、添加二维码
    届时需要更改的部分是：
        1、 模板层：直接做一个a标签，herf按照当前页面设备ID写死，直接请求到download路由上
        2、 视图层：仅保留一个下载函数，通过识别前端的传回的ID，到数据库中请求数据并传至前端，提供下载
        3、 模型层：设备表 增加字段1 设备图像 增加字段2 二维码 出库单表 增加字段1 二维码
    目前二维码实现逻辑：
        前端——（请求{设备ID}）——>服务器（实时生成二维码）——（响应{二维码}）——>前端
'''

def msg_success(code, msg, *args, **kwargs):
    '''
    用于回传服务器响应
    :param code: 01->成功；02->已知错误；03->未知错误
    :param msg: 响应文本，描述响应情况
    :param args: 【可选】
    :param kwargs: 【可选】
    :return: Json格式数据
    '''
    return JsonResponse({'code': code, 'msg': msg, 'args': args, 'kwargs': kwargs})


def home(request):
    modelOfAssets = Assets.objects
    modelOfTables = Tables.objects
    modelOfEvents = Events.objects.all().order_by('date').reverse()
    return render(request, template_name='assets/home.html', context={
        'aa': modelOfAssets.count(),
        'ao': modelOfAssets.filter(St=True).count(),
        'ai': modelOfAssets.filter(St=False).count(),
        'oa': modelOfTables.count(),
        'eventslist': modelOfEvents,
    })


def assets(request):
    metching = Assets.objects.all()
    return render(request, template_name='assets/assetslist.html', context={'itemlist': metching})


def outgoing(request):
    metching = Tables.objects.all()
    return render(request, template_name='assets/outgoinglist.html', context={'itemlist': metching})


def assetdetail(request, aid):
    metching = Assets.objects.all().filter(No=aid)[0]
    try:
        metching_events = Events.objects.filter(As=aid).order_by('Dt').reverse()
    except:
        metching_events = None
    try:
        metching_files = Files.objects.all().filter(As=aid)
    except:
        metching_files = None
    return render(request, template_name='assets/assetsdetail.html', context={
        'asset': metching,
        'events': metching_events,
        'files': metching_files,
    })


def outgoingdetail(request, oid):
    if request.method == "GET":
        metching = Tables.objects.get(Number_form=oid)
        metch_records = RecordTables.objects.filter(Table=metching).select_related("Asset").all()
        return render(request, template_name='assets/outgoingdetail.html', context={
            'outgoing': metching,
            'assets': metch_records,
        })


@csrf_exempt
def add(request, oid):
    if request.method == 'GET':
        metching = Assets.objects.filter(St=False)
        project_outgoing = Tables.objects.get(Number_form=oid).Project
        number_outgoing = Tables.objects.get(Number_form=oid).Number_form
        return render(request, template_name='assets/createoutgoing select assets.html',
                      context={'itemlist': metching, 'project': project_outgoing, 'number': number_outgoing,
                               'oid': oid})


def loadrecord(request):
    nowdaydate = datetime.datetime.now()
    name = request.POST.get('name')
    table = 'Tables'
    remark1 = fr"{nowdaydate.strftime('%d-%m-%Y %H:%M:%S')} {name} 在 {table} 中 添加了一条记录"
    remark2 = fr"{nowdaydate.strftime('%d-%m-%Y %H:%M:%S')} {name} 在 {table} 中 添加了一条记录"


def download(request, eid):
    if eid[-1] == 'A':
        '''返回资产条形码'''
        f = open(f"{eid[0:-2]}_temp_QRcode.png", 'rb')
        return FileResponse(f, as_attachment=True, filename=f"{eid}.png")
    elif eid[-1] == 'T':
        '''返回出库单条形码'''
        f = open(f"{eid[0:-2]}_temp_QRcode.png", 'rb')
        return FileResponse(f, as_attachment=True, filename=f"{eid}.png")


def test(request):
    print(request.POST['mes'])


def outlet(request):
    """创建出库单"""
    if request.method == 'GET':
        return render(request, template_name='assets/createoutgoing.html',
                      context={'No': '提交后系统自动生成', 'Dt': '提交后系统自动生成'})


def outgoing_post(request):
    print('ok')
    '''
    不接受任何GET请求，只对POST请求进行分析并响应
    之后将所有的关于出库表增删改查的POST请求统统编号一个code
    放在这个视图函数内
    同时所有的POST请求均不在使用明文，一律使用密文
    :param request:
    :return:
    '''
    if request.method == 'POST':
        if request.POST.get('code') == '1':
            '''创建出库单'''
            post = request.POST
            now_time = datetime.datetime.strftime(datetime.datetime.now(), "%y%m%d%H%M%S")
            Tables.objects.create(
                Name_person=post.get('na_j'),
                Create_time=datetime.datetime.now(),
                Start_date=post.get('db_j'),
                End_date=post.get('de_j'),
                Project=post.get('po_j'),
                Status='进行',
                Number_form='YXBZ-' + now_time
            )
            Events.objects.create(context=f"{post.get('na_j')} 创建了新项目 {post.get('po_j')}")
            return JsonResponse({
                'code': 1,
                'mes': '出库单创建成功',
                'no': 'YXBZ-' + now_time
            })
        elif request.POST.get('code') == '2':
            '''向出库单添加资产'''
            metching_outgoing = Tables.objects.get(Number_form=request.POST['outgoing_id'])
            metching_assets = Assets.objects.get(No=request.POST['asset_id'])
            metching_assets.St = True
            metching_assets.Po = request.POST['outgoing_id']
            metching_assets.save()
            Events.objects.create(context=f"{metching_outgoing}借出{metching_assets}")
            RecordTables.objects.create(Table=metching_outgoing, Asset=metching_assets)
            return JsonResponse({
                'code': '1',
                'mes': '添加成功'
            })
        elif request.POST.get('code') == '3':
            '''出库单归档'''
            metch_outgoing = Tables.objects.get(Number_form=request.POST.get('outgoing_id'))
            metch_outgoing.Status = '结束'
            metch_outgoing.save()
            Events.objects.create(context=f"归档项目 {metch_outgoing}")
            return JsonResponse({
                'code': '1',
                'mes': '归档成功'
            })
        elif request.POST.get('code') == '4':
            '''单个归还物资'''
            print(1, request.POST['asset_id'])
            metch_asset = Assets.objects.get(No=request.POST.get('asset_id'))
            metch_asset.St = False
            metch_asset.Po = None
            metch_asset.save()
            Events.objects.create(context=f"归还物资 {metch_asset}")
            return JsonResponse({
                'code': '1',
                'mes': '归还成功'
            })
        elif request.POST.get('code') == '5':
            '''从出库单中删除单个物资，一般指错误的添加了某个物资'''
            metch_table = Tables.objects.get(Number_form=request.POST.get('outgoing_id'))
            metch_asset = Assets.objects.get(No=request.POST.get('asset_id'))
            metch_asset.St = False
            metch_asset.Po = None
            metch_asset.save()
            Events.objects.create(context=f"由于选取失误物资已归还 {metch_asset}")
            RecordTables.objects.get(Table=metch_table, Asset=metch_asset).delete()
            return JsonResponse({
                'code': '1',
                'mes': '删除成功'
            })
        elif request.POST.get('code') == '6':
            '''请求生成物资二维码'''
            metch_asset = Assets.objects.get(No=request.POST.get('asset_id'))
            barcode_genor(data={
                'item_id':metch_asset.No,
                'asset_name':metch_asset.Na,
                'website_url':root_url,
                'asset_model': metch_asset.Mo,
                'asset_Location':metch_asset.Lo,
                })
            return JsonResponse({
                'code': '1',
                'mes': f'二维码生成完毕，点击确定开始下载:{metch_asset.No}',
                'download_url': f"{metch_asset.No}-A"
            })
        elif request.POST.get('code') == '7':
            '''请求生成出库单二维码'''
            metch_table = Tables.objects.get(Number_form=request.POST.get('outgoing_id'))
            barcode_genor(data={
                'item_id': metch_table.Number_form,
                'table_title': metch_table.Project,
                'website_url': root_url,
                'table_chief': metch_table.Name_person,
                'table_beginning_date': metch_table.Start_date,
                'table_ending_date': metch_table.End_date,
            })
            return JsonResponse({
                'code': '1',
                'mes': f'二维码生成完毕，点击确定开始下载:{metch_table.Number_form}',
                'download_url': f"{metch_table.Number_form}-T"
            })

    if request.method == 'GET':
        return render(request, template_name='assets/error.html', )


def barcode_genor(data):
    img = qrcode.make(data)
    img.save(f"{data['item_id']}_temp_QRcode.png")