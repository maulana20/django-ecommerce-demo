from django.shortcuts import get_object_or_404, render
from django.db.models import Count

from account.models import UserBase

def chat_inbox(request):
    users = []
    for user in request.user.comments_to.all().values('user').annotate(total=Count('id')).order_by():
        users.append(UserBase.objects.get(id=user['user']))
    
    return render(request, 'chat/home.html', {'users': users})

def chat_sent(request):
    
    users = []
    for recipient in request.user.comments_from.all().values('recipient').annotate(total=Count('id')).order_by():
        users.append(UserBase.objects.get(id=recipient['recipient']))
    
    return render(request, 'chat/home.html', {'users': users})
