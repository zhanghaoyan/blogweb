from django.shortcuts import render,redirect,HttpResponse
from django import forms
from django.forms import fields,widgets
from backend import models
from django.utils.safestring import mark_safe
import hashlib,math

# Create your views here.

def auth(func):
    def inner(request,*args,**kwargs):
        if request.session.get("is_login",None):
            return func(request,*args,**kwargs)
        else:
            return redirect("/login/")
    return inner

def calculate_hash(hashstr,salt):
    salt = salt.encode()
    str = hashstr.encode()
    hash = hashlib.md5(salt)
    hash.update(str)
    res = hash.hexdigest()
    return res

def pageold(request,date_list,per_p_count=3,dis_page_num=5):
    # 用户点击的当前页面页码
    current_page = request.GET.get('p',1)
    current_page = int(current_page)
    # 所有数据的长度，决定我们需要多少分页
    data_len = len(date_list)
    # 每个页面上显示多少条数据
    per_page_count = per_p_count
    # 用于将数据切片的起始位置，根据当前页的页码生成切片的起始位置
    start = (current_page - 1) * per_page_count
    # 用于将数据切片的终止位置，根据当前页面页码生成切片的终止位置
    end = current_page * per_page_count
    # 根据总数据长度和每页显示的数据条目相除商和余数，余数不为0时，总页码加一
    page_count,last = divmod(data_len,per_page_count)
    if last:
        page_count += 1
    # 对数据切片
    li = date_list[start:end]
    # 声明变量用于存放生成的翻页按钮的字符串
    link_list = []
    # 页面上要显示的翻页按钮的数量，最好写成奇数，页面生成的页码才对称
    if data_len/per_page_count >= dis_page_num:
        display_page_num = dis_page_num
    else:
        display_page_num = math.ceil(data_len/per_page_count)
    # 如果当前请求的页面小于等于页面显示页码数的中位数，那么页码起始位置为1，结束位置为显示页码数加一
    if current_page <= math.ceil((display_page_num + 1)/2):
        page_start = 1
        page_end = display_page_num + 1
    else:
        # 如果当前页码位于总页码后几项，那么起始位置就是总页码减去显示页码数量，结束页码就是总页码加一
        if current_page > page_count - int((display_page_num + 1)/2):
            page_end = page_count + 1
            page_start = page_count - display_page_num
        else:
            # 否则，终止页码就是当前页码加上显示页码加一后的一半
            page_end = current_page + int((display_page_num + 1)/2)
            # 否则，起始页码就是当前页码减去显示页码减一后的一半
            page_start = current_page - int((display_page_num - 1)/2)
    # 将起始页码和终止页码加入range()生成页码字符串
    for item in range(page_start,page_end):
        # 如果当前页码被选中，就为当前页码添加一个css样式active，用于标识当前的页码
        if item == current_page:
            tmp = '<li class="page active"><a href="/?p=%s">%s</a></li>' %(item,item)
        else:
            tmp='<li class="page"><a href="/?p=%s">%s</a></li>' %(item,item)
        # 把所有的页码字符串加入页码字符串列表
        link_list.append(tmp)
    else:
        if display_page_num == 1:
            last = '<li><a href="" class="disabled button big previous">上一页</a></li>'
            next_p = '<li><a href="" class="disabled button big next">下一页</a></li>'
        else:
            if current_page == 1:
                last = '<li><a href="" class="disabled button big previous">上一页</a></li>'
                next_p = '<li><a href="/?p=2" class="button big next">下一页</a></li>'
            elif current_page == page_end-1:
                last = '<li><a href="/?p=%s" class="button big previous">上一页</a></li>' %(current_page-1)
                next_p = '<li><a href="" class="disabled button big next">下一页</a></li>'
            else:
                last = '<li><a href="/?p=%s" class="button big previous">上一页</a></li>' %(current_page-1)
                next_p = '<li><a href="/?p=%s" class="button big next">下一页</a></li>' %(current_page+1)
        link_list.insert(0,last)
        link_list.append(next_p)
    # 成成页码html字符串
    link_str = "".join(link_list)
    # 声明该字符串为安全字符串，页面上显示为html代码
    link_str = mark_safe(link_str)
    return {"li":li,"page":link_str}

def page(request,data):
    current_click_page = request.GET.get('p',1)
    current_click_page = int(current_click_page)
    data_length = len(data)
    per_page_display_data_num = 3
    max_link_num = 5
    link_count, tag = divmod(data_length, per_page_display_data_num)
    if tag:
        link_count += 1
    if data_length >= per_page_display_data_num * max_link_num:
        link_num = max_link_num
        if current_click_page <= (link_num + 1)/2:
            link_start = 1
            link_end = link_num + 1
        elif current_click_page > link_count - int((link_num + 1)/2):
            link_start = link_count - link_num + 1
            link_end = link_count + 1
        else:
            link_start = current_click_page - int((link_num - 1)/2)
            link_end = current_click_page + int((link_num - 1)/2) + 1
    else:
        link_num,last = divmod(data_length,per_page_display_data_num)
        if last:
            link_num += 1
            link_start = 1
            link_end = link_start + link_num
    display_start_data_pos = (current_click_page - 1) * per_page_display_data_num
    display_end_data_pos = current_click_page * per_page_display_data_num
    display_data = data[display_start_data_pos:display_end_data_pos]
    link_list = []
    if current_click_page != 1:
        tmp = '<li><a href="/?p=%s" class="button big previous">上一页</a></li>' %(current_click_page - 1)
    else:
        tmp = '<li><a class="disabled button big previous">上一页</a></li>'
    link_list.append(tmp)
    for item in range(link_start,link_end):
        if item == current_click_page:
            tmp = '<li class="page active"><a href="/?p=%s">%s</a></li>' %(item,item)
        else:
            tmp = '<li class="page"><a href="/?p=%s">%s</a></li>'%(item,item)
        link_list.append(tmp)
    if link_end - 1 == current_click_page:
        tmp = '<li><a class="disabled button big previous">下一页</a></li>'
    else:
        tmp = '<li><a href="/?p=%s" class="button big previous">下一页</a></li>' %(current_click_page + 1)
    link_list.append(tmp)
    # tmp = '<li><a href="/p=%s">最后一页</a></li>' % (link_count)
    # link_list.append(tmp)
    link_str = "".join(link_list)
    link_str = mark_safe(link_str)
    # print("current_click_page:%s data_length:%s link_num:%s link_count:%s link_start:%s link_end:%s " %(current_click_page,data_length,link_num,link_count,link_start,link_end))
    return {"li":display_data,"page":link_str}

class LoginFrom(forms.Form):
    username = forms.CharField(
        error_messages={"required":"用户名不能为空"},
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"用户名","id":"username"}),
    )
    passwd = forms.CharField(
        error_messages={"required":"密码不能为空"},
        widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"密码","id":"passwd"}),
    )

def login(request):
    if request.method == "GET":
        obj = LoginFrom()
        return render(request,"login.html",{"obj":obj})
    else:
        obj = LoginFrom(request.POST)
        tag = obj.is_valid()
        if tag:
            data = obj.cleaned_data
            username = data["username"]
            pwd = data["passwd"]
            passwd = calculate_hash(pwd,"0hy1ovOL")
            auth_result = models.User.objects.filter(username=username,passwd=passwd)
            if auth_result:
                request.session['username'] = username
                request.session['is_login'] = True
                return redirect("/")
            else:
                return redirect("/login/")
        else:
            return render(request,"login.html",{"obj":obj})

def logout(request):
    request.session.clear()
    return redirect("/")

def index(request):
    user_status = request.session.get("is_login")
    userdata = ""
    url = ""
    urltext = ""
    if user_status:
        url = "/logout/"
        urltext = "注销"
        userdata = """
        <li>
            <a href="#">
                <h3>欢迎登录:%s</h3>
            </a>
        </li>
        <li>
            <a href="/backend/index/">
                <h3>管理我的博客</h3>
            </a>
        </li>
        <li>
            <a href="/backend/new_article/">
                <h3>写博客</h3>
            </a>
        </li>""" % request.session.get('username')
    else:
        url = "/login/"
        urltext = "登录"
        userdata = """
        <li>
            <a href="#">
                <h3>请登录</h3>
            </a>
        </li>
        """
    data = models.Article.objects.filter(status=1).all().values()
    res = []
    for item in data:
        res.append(item)
    res.reverse()
    res_dic = page(request,res)
    page_str = res_dic["page"]
    page_data = res_dic["li"]
    return render(request,"index.html",{"data":page_data,"url":url,"urltext":urltext,"userdata":userdata,"page_str":page_str})

def category(request):
    if request.method == "GET":
        user_status = request.session.get("is_login")
        userdata = ""
        url = ""
        urltext = ""
        if user_status:
            url = "/logout/"
            urltext = "注销"
            userdata = """
                <li>
                    <a href="#">
                        <h3>欢迎登录:%s</h3>
                    </a>
                </li>
                <li>
                    <a href="/backend/index/">
                        <h3>管理我的博客</h3>
                    </a>
                </li>
                <li>
                    <a href="/backend/new_article/">
                        <h3>写博客</h3>
                    </a>
                </li>""" % request.session.get('username')
        else:
            url = "/login/"
            urltext = "登录"
            userdata = """
                <li>
                    <a href="#">
                        <h3>请登录</h3>
                    </a>
                </li>
                """
        category_dict = {"linux":1,"python":2,"chat":3,"other":4}
        cid = category_dict.get(request.GET.get("page"))
        if cid:
            data = models.Article.objects.filter(status=1,category=cid).all().values()
            res = []
            for item in data:
                res.append(item)
            res_dic = page(request, res)
            page_str = res_dic["page"]
            page_data = res_dic["li"]
            return render(request,"index.html",{"data":page_data,"url":url,"urltext":urltext,"userdata":userdata,"page_str":page_str})

def detail(request,*args,**kwargs):
    user_status = request.session.get("is_login")
    userdata = ""
    url = ""
    urltext = ""
    if user_status:
        url = "/logout/"
        urltext = "注销"
        userdata = """
        <li>
            <a href="#">
                <h3>欢迎登录:%s</h3>
            </a>
        </li>
        <li>
            <a href="/backend/index/">
                <h3>管理我的博客</h3>
            </a>
        </li>
        <li>
            <a href="/backend/new_article/">
                <h3>写博客</h3>
            </a>
        </li>""" % request.session.get('username')
    else:
        url = "/login/"
        urltext = "登录"
        userdata = """
        <li>
            <a href="#">
                <h3>请登录</h3>
            </a>
        </li>
        """
    aid = args[0]
    data = models.Article.objects.filter(aid=aid).values_list()
    return render(request,"detail.html",{"data":data,"url":url,"urltext":urltext,"userdata":userdata})