from rest_framework import serializers
from .models import CustomUser, Question, Reply


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name',
                  'last_name', 'pass_show']  # Add all relevant fields here
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use create_user method to handle password hashing
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    question = serializers.StringRelatedField()
    
    class Meta:
        model = Reply
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
