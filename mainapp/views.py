from django.shortcuts import render

# 首頁
def home(request):
    return render(request, 'home.html')

# 上傳檔案的視圖函數
def upload(request):
    return render(request, 'upload.html')

# 檔案列表的視圖函數
def file_list(request):
    return render(request, 'file_list.html')

# 登入視圖
def login_view(request):
    return render(request, 'login.html')

# 註冊視圖
def register(request):
    return render(request, 'register.html')
