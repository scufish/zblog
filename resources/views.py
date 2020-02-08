from django.shortcuts import render, redirect
from resources.models import PrivateUser ,Resource
from django.contrib import messages


# Create your views here.


def resource_signin(req):
    if req.session.has_key('isLogin'):
        return redirect('/resource')
    if 'username' in req.COOKIES and 'password' in req.COOKIES:
        username = req.COOKIES['username']
        password = req.COOKIES['password']
    else:
        username = ''
        password = ''
    return render(req, 'resources/resource_signin.html', {
        'username': username,
        'password': password
    })


def quit(req):
    if req.session.has_key('isLogin'):
        req.session.flush()
        messages.add_message(req, messages.SUCCESS, '注销成功', extra_tags='success')
    return redirect('/resource_signin')


def resource(req):
    if req.session.has_key('isLogin'):
        username = req.session.get('username')
        return render(req, 'resources/resource.html', {
            'username': username
        })

    Info = req.POST
    try:
        user = PrivateUser.object.get(username=Info['username'])
    except:
        messages.add_message(req, messages.ERROR, '用户名或者密码错误', extra_tags='success')
        return redirect('/resource_signin')
    if user is not None:
        if Info['password'] == user.password:
            messages.add_message(req, messages.SUCCESS, '登陆成功', extra_tags='success')
            res = render(req, 'resources/resource.html', {
                'username': user.username
            })
            if Info.get('isCookie') == 'on':
                res.set_cookie('username', user.username, max_age=3600 * 24 * 14)
                res.set_cookie('password', user.password, max_age=3600 * 24 * 14)
            req.session['isLogin'] = True
            req.session['username'] = user.username
            return res
        else:
            messages.add_message(req, messages.ERROR, '用户名或者密码错误', extra_tags='error')
            return redirect('/resource_signin')


def register(req):
    # 核验两次密码是否一致
    # 核验用户名是否已经存在
    # 核验通过密文是否正确
    Info = req.POST
    pass1 = Info.get('password1')
    pass2 = Info.get('password2')
    username = Info.get('username')
    email = Info.get('email')
    key = Info.get('key')
    if pass1 is None or pass2 is None or username is None or email is None or key is None:
        messages.add_message(req, messages.ERROR, '出现错误', extra_tags='error')
        return redirect('/debug')
    if pass1 != pass2:
        messages.add_message(req, messages.ERROR, '两次密码不一致', extra_tags='error')
        return redirect('/resource_signin')
    try:
        U=PrivateUser.object.get(username=username)
        messages.add_message(req, messages.ERROR, '该用户名已经被占用了', extra_tags='error')
        return redirect('/resource_signin')
    except:
        pass

    if key != '201510':
        messages.add_message(req, messages.ERROR, '通关密文不正确', extra_tags='error')
        return redirect('/resource_signin')

    newUser = PrivateUser()
    try:
        newUser.username = username
        newUser.email = email
        newUser.password = pass1
        newUser.save()
        messages.add_message(req, messages.ERROR, '注册成功！', extra_tags='success')
        return redirect('/resource_signin')
    except:
        messages.add_message(req, messages.ERROR, '出现错误', extra_tags='error')
        return redirect('/resource_signin')



def submit(req):
    Info = req.POST
    subject  =Info.get('subject')
    href = Info.get('href')
    tag = Info.get('tag')
    key =Info.get('key')
    if req.session.has_key('isLogin'):
        username = req.session.get('username')
        try:
            author =PrivateUser.object.get(username=username)
        except:
            messages.add_message(req, messages.ERROR, '提交失败', extra_tags='error')
            return redirect('/resource')
        newResource = Resource()
        try:
            newResource.key=key
            newResource.author=author
            newResource.subject=subject
            newResource.href=href
            newResource.tag=tag
            newResource.save()
        except:
            messages.add_message(req, messages.ERROR, '提交失败', extra_tags='error')
            return redirect('/resource')
        messages.add_message(req, messages.ERROR, '提交成功！', extra_tags='success')
        return redirect('/resource')
    else:
        messages.add_message(req, messages.ERROR, '提交失败', extra_tags='error')
        return redirect('/resource')

