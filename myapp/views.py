from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict

def test(request):
    return HttpResponse("Hello World")
def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET['cName']
        # print(cName)
        # resultObject = students.objects.filter(cName=cName)
        resultObject = students.objects.filter(cName__contains=cName)
    else:
        resultObject = students.objects.all().order_by("-cID")
    # for d in resultObject:
    #     print(model_to_dict(d))

    # return HttpResponse("Hello World")
    errormessage=""
    if not resultObject:
        errormessage="無此資料"

    return render(request, "search_list.html",locals())

def search_name(request):
    # return HttpResponse("Hello World")
    return render(request, "search_name.html")
from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去前後空白
        # print(site_search)
        #多個關鍵字
        keyworks = site_search.split() #切割字元
        print(keyworks)
        # resultList=[]
        q_objects = Q()
        for keywork in keyworks:
            q_objects.add(Q(cName__contains=keywork),Q.OR)
            q_objects.add(Q(cBirthday__contains=keywork),Q.OR)
            q_objects.add(Q(cEmail__contains=keywork),Q.OR)
            q_objects.add(Q(cPhone__contains=keywork),Q.OR)
            q_objects.add(Q(cAddr__contains=keywork),Q.OR)
        resultList = students.objects.filter(q_objects)

        #一個關鍵字
    #     resultList = students.objects.filter(
    #         Q(cName__contains=site_search)|
    #         Q(cBirthday__contains=site_search)|
    #         Q(cEmail__contains=site_search)|
    #         Q(cPhone__contains=site_search)|
    #         Q(cAddr__contains=site_search)
    #     )
    else:
        resultList = students.objects.all().order_by("cID")
    # return HttpResponse("Hello World")
    status = True
    if not resultList:
        errormessage="無此資料"
        status=False
    data_count = len(resultList)
    # print(data_count)
    # for d in resultList:
    #     print(model_to_dict(d))
    # 分頁設定，每頁顯示3筆
    paginator = Paginator(resultList,3)
    # ?page=1
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # print(dir(page_obj))

    return render(request, "index.html",locals())

from django.shortcuts import redirect
def post(request):
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        # return HttpResponse("資料已新增")
        add = students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        return redirect("/index/")

    else:
        return render(request, "post.html",locals())
    
def edit(request,id):
    if request.method == "POST":
        print(id)
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        # return HttpResponse("資料已修改")
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cBirthday = cBirthday
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        return redirect("/index/")
    else:
        # print(id)
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        # return HttpResponse("hello")
        return render(request, "edit.html",locals())
    
def delete(request,id):
    if request.method == "POST":
        print(id)
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        # return HttpResponse("hello")
        return redirect("/index/")
    else:
        print(id)
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        # return HttpResponse("hello")
        return render(request, "delete.html",locals())
    
########################################################
from django.http import JsonResponse
def getAllItems(request):
    resultObject = students.objects.all().order_by("cID")
    # print(type(resultObject))
    # for d in resultObject:
    #     print(model_to_dict(d))
    # object to list
    resultList = list(resultObject.values())
    # print(resultList)
    return JsonResponse(resultList,safe=False)
    # return HttpResponse("hello")

def getItem(request, id):
    try:
        obj = students.objects.get(cID=id)
        resultDict = model_to_dict(obj)
        return JsonResponse(resultDict)
    except:
        return JsonResponse({"error":"Item not found"},status=404)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt #關閉CSRF驗證
def createItem(request):
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item created successfully"})
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item created successfully"})
        add = students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        return JsonResponse({"message":"Item created successfully"})
    except:
        return JsonResponse({"error":"Missing parameters"},status=400)
    
@csrf_exempt #關閉CSRF驗證
def updateItem(request, id):   
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print(f"id={id},cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item updated successfully"})
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print(f"id={id},cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item updated successfully"})    
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cBirthday = cBirthday
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        return JsonResponse({"message":"Item updated successfully"})  
    except:
        return JsonResponse({"error":"Missing parameters"},status=400)  
    
@csrf_exempt #關閉CSRF驗證
def deleteItem(request, id):
    try:
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        return JsonResponse({"message":"Item deleted successfully"})
    except:
        return JsonResponse({"error":"Item not found"},status=404)