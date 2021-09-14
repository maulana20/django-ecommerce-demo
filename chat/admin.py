from django.contrib.admin import ModelAdmin, site
from chat.models import Message

class MessageModelAdmin(ModelAdmin):
    readonly_fields = ('created',)
    search_fields = ('id', 'body', 'user__user_name', 'recipient__user_name')
    list_display = ('id', 'user', 'recipient', 'created', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'created'


site.register(Message, MessageModelAdmin)
