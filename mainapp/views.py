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
@login_required  # 確保只有登入的使用者才能上傳文件
def upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 處理上傳的文件
            document = form.cleaned_data['document']
            s3 = boto3.client('s3')

            # 使用者的 username 作為文件目錄
            user_directory = request.user.username
            file_path = f'{user_directory}/{document.name}'  # 基於 username 儲存文件

            # 將文件上傳到 S3
            try:
                s3.upload_fileobj(document, settings.AWS_STORAGE_BUCKET_NAME, file_path)
            except ClientError as e:
                print(f"Error uploading file: {e}")
                return HttpResponse("Error uploading file.", status=500)

            return redirect('file_list')  # 文件上傳後重定向到文件列表頁面
    else:
        form = DocumentUploadForm()
    return render(request, 'upload.html', {'form': form})

# 檔案列表的視圖函數
@login_required  # 確保只有登入的使用者才能查看文件列表
def file_list(request):
    s3 = boto3.client('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    user_directory = request.user.username  # 使用者的 username 作為文件目錄

    try:
        # 僅列出該使用者目錄下的文件
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'{user_directory}/')
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
@login_required  # 確保只有登入的使用者才能刪除文件
def delete_file(request, file_name):
    s3 = boto3.client('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    user_directory = request.user.username  # 使用者的 username 作為文件目錄

    if request.method == 'POST':
        try:
            # 將 file_name 加上使用者的目錄路徑
            file_key = f'{user_directory}/{file_name}'
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
