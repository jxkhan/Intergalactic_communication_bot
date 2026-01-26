from rest_framework import serializers
from .models import Categories, FAQ , Customer
from django.contrib.auth.password_validation import validate_password


class CustomerSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = [ 'username', 'email', 'password', 'password_confirm']


    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs    

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = Customer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id','name','description','created_at','updated_at']



class FAQSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())

    class Meta:
        model = FAQ
        fields = ['id','question','answer','category','keywords','views','helpful_votes','created_at','updated_at']        


