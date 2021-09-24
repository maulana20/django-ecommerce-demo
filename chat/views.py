from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count

from account.models import UserBase

def chat_message(request):
    
    if hasattr(request.user, 'shop') == True:
        users = { UserBase.objects.get(id=recipient['recipient']) for recipient in request.user.comments_from.all().values('recipient').annotate(total=Count('id')).order_by() if request.user.id != recipient['recipient'] }
    else:
        users = { UserBase.objects.get(id=user['user']) for user in request.user.comments_to.all().values('user').annotate(total=Count('id')).order_by() if request.user.id != user['user'] }
    
    return render(request, 'chat/home.html', {'users': users})
