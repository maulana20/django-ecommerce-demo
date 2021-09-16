from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, CharField

from chat.models import Message
from account.models import UserBase

class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.user_name', read_only=True)
    recipient = CharField(source='recipient.user_name')
    shop_image = CharField(source='user.shop.image', read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(UserBase, user_name=validated_data['recipient']['user_name'])
        
        msg = Message(recipient=recipient, body=validated_data['body'], user=user)
        
        msg.save()
        
        return msg

    class Meta:
        model = Message
        fields = ('id', 'user', 'recipient', 'shop_image', 'created', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('user_name',)
