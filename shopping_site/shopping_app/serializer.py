from rest_framework import serializers
from .models import User, cart,item,cart
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = '__all__'

class cartSerializer(serializers.ModelSerializer):
    product = itemSerializer(many=True, read_only=True) 
    # user = UserSerializer(many = True,read_only = True)
    class Meta:
        model = cart
        fields = '__all__'
