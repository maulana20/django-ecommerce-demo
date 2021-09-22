from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, CharField, ReadOnlyField, SerializerMethodField

from chat.models import Message
from account.models import UserBase, Shop
from store.models import Product

class ShopModelSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ('title', 'image')

class ProductModelSerializer(ModelSerializer):
    absolute_url = ReadOnlyField(source='get_absolute_url')
    
    class Meta:
        model = Product
        fields = ('title', 'image', 'absolute_url')

class MessageModelSerializer(ModelSerializer):
    recipient = CharField(source='recipient.uuid')
    slug = CharField(source='product', allow_blank=True)
    
    user = CharField(source='user.uuid', read_only=True)
    user_name = CharField(source='user.user_name', read_only=True)
    
    shop = ShopModelSerializer(source='user.shop', read_only=True)
    product = ProductModelSerializer(read_only=True)
    
    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(UserBase, uuid=validated_data['recipient']['uuid'])
        product = None if not validated_data['product'] else get_object_or_404(Product, slug=validated_data['product'])
        
        msg = Message(recipient=recipient, body=validated_data['body'], user=user, product=product)
        
        msg.save()
        
        return msg

    class Meta:
        model = Message
        fields = ('id', 'user', 'user_name', 'recipient', 'shop', 'product', 'slug', 'created', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('user_name',)
