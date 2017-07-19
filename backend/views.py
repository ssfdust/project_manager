from django.shortcuts import render
from backend.forms import LoginForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
import logging
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
        logger.debug('get captcha_image_url')
        respon = dict()
        respon['status'] = 'log in'
        respon['captcha_0'] = CaptchaStore.generate_key()
        respon['img_src'] = captcha_image_url(respon['captcha_0'])
        logger.info(respon)
        return JsonResponse(respon)

def is_login(request):
    respon = dict()
    if request.user.is_authenticated:
        respon['status'] = 'login'
        logger.debug('The response is '% respon)
    else:
        response['status'] = 'logout'
    return JsonResponse(respon)

