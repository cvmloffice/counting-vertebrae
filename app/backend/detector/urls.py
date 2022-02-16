from django.urls import path, include
from .views import ImageDetectorView, ImageDetectorReturnImage

urlpatterns = [
    path('', ImageDetectorView.as_view()),
    path('image/', ImageDetectorReturnImage.as_view())

]