from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    # ex : /polls/
    # path('', views.index, name='index'), # polls란 어플리케이션에 대한 path를 설정한다.
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path('specifics/<int:question_id>/', views.detail, name='detail'),
    # ex : /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/results/", views.results, name = "results"),
    # ex : /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]