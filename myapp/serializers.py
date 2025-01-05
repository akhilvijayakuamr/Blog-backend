from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from .models import Post

# User register serializers

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required = True,
    validators = [UniqueValidator(queryset=CustomUser.objects.all(),message="Email Already Exists")]
    )
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only':True}
        }
        
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
   
# Login serializer

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
    
# All post serializer


class AllPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    postId = serializers.IntegerField(source='id')
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField()
    created_at = serializers.DateTimeField()
    
    