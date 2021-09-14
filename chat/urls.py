from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter

from chat.api import MessageModelViewSet, UserModelViewSet, InboxModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')
router.register(r'user-inbox', InboxModelViewSet, basename='user-inbox-api')

app_name = 'chat'

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    
    path('inbox', login_required(TemplateView.as_view(template_name='chat/inbox.html')), name='inbox'),
]
