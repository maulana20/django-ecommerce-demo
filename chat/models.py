from django.db import models
from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Message(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='user', related_name='comments_from', db_index=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='recipient', related_name='comments_to', db_index=True)
    
    body = models.TextField(max_length=500, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'messages'
        ordering = ('created',)
    
    def __str__(self):
        return str(self.id)
    
    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)
    
    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)
    
    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(Message, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()
