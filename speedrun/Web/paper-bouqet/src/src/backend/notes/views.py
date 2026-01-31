from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import Note, AdminUser
import json
import yaml

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        action = request.POST.get('action')
        
        if action == 'user_login':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'User login successful', 'action': action})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
        elif action == 'admin_login':
            try:
                admin_user = AdminUser.objects.get(username=username, is_active=True)
                if check_password(password, admin_user.password):
                    request.session['admin_id'] = admin_user.id
                    return JsonResponse({'success': True, 'message': 'Admin login successful', 'action': action})
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
            except AdminUser.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        action = request.POST.get('action')
        
        if action == 'user_register':
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)
            
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'success': True, 'message': 'User created successfully', 'action': action})
        elif action == 'admin_register':
            if AdminUser.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Admin username already exists'}, status=400)
            
            admin_user = AdminUser.objects.create(
                username=username,
                password=make_password(password)
            )
            return JsonResponse({'success': True, 'message': 'Admin created successfully', 'action': action})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def notes_list(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        notes_data = []
        for note in notes:
            notes_data.append({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'username': note.username,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            })
        return JsonResponse({'notes': notes_data})
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        username = request.POST.get('username', '')
        
        note = Note.objects.create(
            title=title,
            content=content,
            username=username
        )
        return JsonResponse({
            'success': True,
            'note': {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'username': note.username,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            }
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def is_admin_authenticated(request):
    return 'admin_id' in request.session and AdminUser.objects.filter(
        id=request.session['admin_id'], is_active=True
    ).exists()

@csrf_exempt
def debug(request):
    if not is_admin_authenticated(request):
        return JsonResponse({'error': 'Admin authentication required'}, status=401)
    
    if request.method == 'POST':
        yaml_content = request.POST.get('yaml_content')
        
        if not yaml_content:
            return JsonResponse({'error': 'yaml_content parameter required'}, status=400)
        
        try:
            yaml.load(yaml_content,Loader=yaml.UnsafeLoader)
            return JsonResponse({
                'success': True,
            })
        except yaml.YAMLError as e:
            return JsonResponse({'error': f'YAML parsing error'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
