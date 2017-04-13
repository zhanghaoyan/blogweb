from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.forms import widgets
import time,json
from backend import models
from index.views import auth

# Create your views here.

class Edit(forms.Form):
    title = forms.CharField(
        widget=widgets.TextInput(attrs={"id":"title","class":"input-self"}),
        error_messages={"required":"标题不能为空"}
    )
    content = forms.CharField(
        required=False,
        widget=widgets.Textarea(attrs={"id":"content"}),
    )

    category_id = forms.Field(
        widget=widgets.RadioSelect(choices=((1,"LINUX"),(2,"PYTHON"),(3,"废点话"),(4,"瞎玩儿"))),
    )

@auth
def index(request):
    return render(request,"backend/index.html")

@auth
def upload(request):
    if request.method == "POST":
        callback = request.GET.get('CKEditorFuncNum')
        file = request.FILES.get("upload")
        filepath = "static/imgupload/%s" %file
        with open(filepath,"wb+") as f:
            for line in file.chunks():
                f.write(line)
        res = "<script>window.parent.CKEDITOR.tools.callFunction(%s,'/%s', '');</script>" %(callback,filepath)
        return HttpResponse(res)

@auth
def article_list(request):
    if request.method == "GET":
        data = models.Article.objects.filter(status=1).all().values("aid","title","time","category__cname")
        return render(request,"backend/article_list.html",{'data':data})
    elif request.method == "POST":
        pass

@auth
def new_article(request):
    if request.method == "GET":
        obj = Edit()
    elif request.method == "POST":
        obj = Edit(request.POST)
        tag = obj.is_valid()
        if tag:
            data = obj.cleaned_data
            localtime = time.localtime()
            Time = time.strftime("%Y-%m-%d %H:%M:%S",localtime)
            data['time'] = Time
            models.Article.objects.create(**data)
            return redirect("/backend/index/")
    else:
        return redirect("/")
    return render(request,"backend/new_article.html",{"obj":obj})

@auth
def edit(request):
    if request.method == "GET":
        return redirect("/backend/new_article/")
    elif request.method == "POST":
        edit_aid = request.POST.get("aid")
        model_data = models.Article.objects.filter(aid=edit_aid).values("aid","title","content","time","category_id","category__cname")
        for item in model_data:
            dic = item
        data = Edit(dic)
        return render(request,"backend/edit_article.html",{"obj":data})

@auth
def edit_article(request):
    if request.method == "POST":
        edit_aid = request.POST.get("edit_aid")
        title = request.POST.get("title")
        category_id = request.POST.get("category_id")
        content = request.POST.get("content")
        localtime = time.localtime()
        Time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
        data = {"aid":edit_aid,"title":title,"category_id":category_id,"content":content,"time":Time,"status":1}
        models.Article.objects.filter(aid=edit_aid).update(**data)
        return redirect("/backend/index/")

@auth
def save_draft(request):
    if request.method == "POST":
        obj = Edit(request.POST)
        tag = obj.is_valid()
        if tag:
            data = obj.cleaned_data
            aid = request.POST.get("edit_aid")
            localtime = time.localtime()
            Time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
            data['time'] = Time
            data["status"] = 2
            if not aid:
                models.Article.objects.create(**data)
            else:
                models.Article.objects.filter(aid=aid).update(**data)
            return redirect("/backend/index/")

@auth
def draft(request):
    if request.method == "GET":
        data = models.Article.objects.filter(status=2).all().values("aid","title","time","category__cname")
        return render(request,"backend/article_list.html",{'data':data})

@auth
def delete(request):
    if request.method == "POST":
        delete_type = request.POST.get("type_id")
        delete_aid = request.POST.get("aid")
        response_dic = {}
        try:
            models.Article.objects.filter(aid=delete_aid).update(status=delete_type)
            response_dic['status'] = "OK"
        except Exception as e:
            print(e)
            response_dic['status'] = "Error"
        return HttpResponse(json.dumps(response_dic))

@auth
def recycle(request):
    if request.method == "GET":
        data = models.Article.objects.filter(status=3).all().values("aid","title","time","category__cname")
        return render(request,"backend/article_list.html",{'data':data})

@auth
def test(request):
    data = Edit({"title": "aaaa", "content": "bbbb", "category_id": 3})
    return render(request,"backend/new_article.html",{"obj":data})