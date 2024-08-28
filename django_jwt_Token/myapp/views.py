from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
import jwt
from datetime import datetime, timedelta
from functools import wraps
from django.conf import settings

def token_required(func):
    @wraps(func)
    def decorated(request, *args, **kwargs):
        token = request.GET.get('token')
        if not token:
            return JsonResponse({'Alert': 'Token is missing'}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'Alert': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'Alert': 'Invalid Token!'}, status=401)
        return func(request, *args, **kwargs)
    return decorated

def home(request):
    if not request.session.get("logged_in"):
        return render(request, 'login.html')
    else:
        return HttpResponse('Logged in Currently')

def public(request):
    return HttpResponse('For Public')

@token_required
def auth(request):
    return HttpResponse('JWT is verified. Welcome to the page')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'rahul' and password == 'rahul':
            request.session['logged_in'] = True

            token = jwt.encode({
                'user': username,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, settings.SECRET_KEY, algorithm="HS256")

            return JsonResponse({'token': token})
        else:
            response = HttpResponse('Unable to verify', status=403)
            response['WWW-Authenticate'] = 'Basic realm="Authentication Failed!"'
            return response

def logout(request):
    request.session.pop('logged_in', None)
    return HttpResponse('Logged out successfully')
