from django.shortcuts import render
from backend.forms import LoginForm, FrontendActionForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from backend.confparse import CONFIG
from backend.filemanager import FrontendFileStatus, file_handler
from math import ceil
import time
import logging
import os
import json
import re

# Create your views here.

logger = logging.getLogger('django')

@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        respon = dict()
        logger.info('get login post')
        form = LoginForm(request.POST)
        logger.debug('the POST data %s' % request.POST)
        if form.is_valid():
            logger.debug('captcha verified')
            username = form.data['username']
            password = form.data['password']
            if form.data['remember'] == "false":
                request.session.set_expiry(0)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                respon['status'] = 'login success'
                respon['user'] = username
                return JsonResponse(respon)
            else:
                respon['status'] = 'login failed'
                respon['captcha_0'] = CaptchaStore.generate_key()
                respon['img_src'] = captcha_image_url(respon['captcha_0'])
                respon['msg'] = 'Wrong username or password'
                return JsonResponse(respon)
        else:
            logger.info('Login failed with wrong captcha')
            respon['status'] = 'login fail'
            respon['captcha_0'] = CaptchaStore.generate_key()
            respon['img_src'] = captcha_image_url(respon['captcha_0'])
            respon['msg'] = 'Wrong captcha input'
            return JsonResponse(respon)
    else:
        respon = dict()
        if request.user.is_authenticated:
            respon['status'] = 'login success'
            respon['user'] = request.user.get_username()
            logger.info('the user has logined in')
        else:
            logger.debug('get captcha_image_url')
            respon['status'] = 'log in'
            respon['captcha_0'] = CaptchaStore.generate_key()
            respon['img_src'] = captcha_image_url(respon['captcha_0'])
            logger.info(respon)
        return JsonResponse(respon)

def is_login(request):
    respon = dict()
    if request.user.is_authenticated:
        respon['status'] = 'login'
        respon['user'] = request.user.get_username()
        logger.debug('The response is %s'% respon)
        logger.info('Some one has logged in')
    else:
        response['status'] = 'logout'
        logger.info('Some one has not logged in')
    return JsonResponse(respon)

def get_frontend_status(request):
    respon = dict()
    frontend_path = CONFIG['frontend']['uploads']
    if request.method == 'POST':
        logger.info('get_frontend_status api get a request')
        form = FrontendActionForm(request.POST, request.FILES)
        if form.is_valid():
            filename = form.data['filename']
            action = form.data['action']
            page = int(form.data['page'])
            path = frontend_path
            if action == 'upload':
                real_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                upload_file = request.FILES['file']
                filename = 'frontend' + real_time + '.zip'
                action = 'active'
                file_save = os.path.join(frontend_path, filename)
                with open(file_save, 'wb+') as f:
                    for chunk in upload_file.chunks():
                        f.write(chunk)

            # frontend return a dict object
            # it contains a list object called
            # files which includes three properties
            # for each element.
            # files:[
            #     ['filename1', '2003-01-03 23:56:23', False],
            #     ['filename2', '2003-01-03 23:56:23', False],
            # ....
            # ]
            # metadata: {
            #     file_num: 180
            #}
            #ret = frontend_file_handler(frontend_path, filename, action)
    else:
        page = int(request.GET['page'])
        #ret = frontend_file_handler(frontend_path, '', 'get')

    #respon['files'] = ret['files'] if len(ret['files']) == 0 else ret['files'][(page - 1) * 10: (page - 1)* 10 + 1 ]
    #respon['pages'] = ceil(len(ret['files']) / 10)
    respon['status'] = 'success'
    return JsonResponse(respon)
    

