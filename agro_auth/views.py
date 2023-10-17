from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .serializers import CustomUserSerializer, QuestionSerializer, ReplySerializer
from .models import CustomUser, Question, Reply
from django.shortcuts import get_object_or_404


############# AUTHENTICATION ################


@api_view(['GET'])
def index(request):
    api_list = {
        'login': '/login/',
        'logout': '/logout/',
        'register': '/register/',
    }
    return Response(api_list)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_data(request):
    return Response({'message': 'This is secure data!'})


@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def custom_logout(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})


@api_view(['POST'])
def custom_register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Set the password manually
            user.set_password(request.data.get('password'))
            user.save()  # Save the user with the hashed password

            # Create a token for the user
            Token.objects.create(user=user)

            return Response({'message': 'Registration successful', 'token': user.auth_token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################ QUESTION / ANSWERS ####################


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def question_list_create(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    serializer = ReplySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, question=question)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def question_detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)

    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_replies_for_question(request, question_id):
    replies = Reply.objects.filter(question_id=question_id)
    serializer = ReplySerializer(replies, many=True)
    return Response(serializer.data)
