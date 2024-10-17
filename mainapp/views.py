from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, DocumentUploadForm
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse
import os
# 首頁
def home(request):
    return render(request, 'home.html')

# 上傳檔案的視圖函數
def upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 處理上傳的文件
            document = form.cleaned_data['document']
            s3 = boto3.client('s3')

            # 定義文件存儲到 S3 的目錄和文件名
            file_path = f'documents/{document.name}'
            s3.upload_fileobj(document, settings.AWS_STORAGE_BUCKET_NAME, file_path)

            return redirect('file_list')  # 文件上傳後重定向到文件列表頁面
    else:
        form = DocumentUploadForm()
    return render(request, 'upload.html')

# 檔案列表的視圖函數
def file_list(request):
    s3 = boto3.client('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix='documents/')
        files = response.get('Contents', [])
        print(files)
        for file in files:
            file['url'] = f"https://{bucket_name}.s3.amazonaws.com/{file['Key']}"
            file['name'] = os.path.basename(file['Key'])
            if file['Size'] < 1000:
                file['size_display'] = f"{file['Size']} bytes"
            elif file['Size'] < 1000000:
                file['size_display'] = f"{file['Size'] / 1000:.2f} KB"
            else:
                file['size_display'] = f"{file['Size'] / 1000000:.2f} MB"
    except ClientError as e:
        print(f"Error listing files: {e}")
        files = []

    return render(request, 'file_list.html', {'files': files})

# delete_file
def delete_file(request, file_name):
    s3 = boto3.client('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    if request.method == 'POST':
        try:
            # 將 file_name 加上 'documents/' 路徑
            file_key = f'documents/{file_name}'
            s3.delete_object(Bucket=bucket_name, Key=file_key)
            return redirect('file_list')
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return HttpResponse("Error deleting file.", status=500)

    return redirect('file_list')

# 登入視圖
def login_view(request):
    return render(request, 'login.html')

# 註冊視圖
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 儲存新使用者
            login(request, user)  # 自動登入新註冊的使用者
            return redirect('home')  # 註冊成功後重定向到首頁
    else:
        form = CustomUserCreationForm(request.POST)
    
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')
