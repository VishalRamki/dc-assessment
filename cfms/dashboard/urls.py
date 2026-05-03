from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("complaint/", views.IndexView.as_view(), name="index"),
    path("complaint/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path('complaint/create/', views.CreateView.as_view(), name='create'),
    path("complaint/<int:pk>/status/<int:status_id>/",views.UpdateComplaintStatusView.as_view(), name="update-status")
]