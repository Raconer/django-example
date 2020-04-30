"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path() 함수에는 2개의 필수 인수인 route와 view, 2개의 선택 가능한 인수로
    # ksargs(Key Word arguments)와 name까지 모두 4개의 인수가 전달 되었다.
    path('polls/', include('polls.urls')), # application url path를 지정해 둔다.
    path('admin/', admin.site.urls),
]
