from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from chat.serializers import MessageModelSerializer, UserModelSerializer
from chat.models import Message
from account.models import UserBase

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageModelSerializer
    
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) | Q(user=request.user))
        target = self.request.query_params.get('target', None)
        
        if target is not None:
            self.queryset = self.queryset.filter(Q(recipient=request.user, user__user_name=target) | Q(recipient__user_name=target, user=request.user))
        
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(self.queryset.filter(Q(recipient=request.user) | Q(user=request.user), Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserModelSerializer
    
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
