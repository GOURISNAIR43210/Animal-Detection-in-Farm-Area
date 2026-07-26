from django.contrib import admin
from django.urls import path
from detection import views

# 🔥 IMPORTANT FOR VIDEO
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home),
    path('detect/', views.detect),
    path('result/', views.result_page),
    path('get-result/<str:id>/', views.get_result),
]

# 🔥 THIS LINE FIXES VIDEO PLAYING
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)