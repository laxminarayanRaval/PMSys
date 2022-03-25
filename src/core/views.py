from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView  # User Register

from .serializers import ProjectSerializer, RegisterSerializer
from .models import Project
from django.contrib.auth.models import User


# Testing API
"""
class TestView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        print('Auth User:', request.user)
        qs = Project.objects.all()
        serializer = ProjectSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
"""


class RegisterView(CreateAPIView):
    qs = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qs = Project.objects.all()
        serializer = ProjectSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, *args, **kwargs):
        qs = Project.objects.get(pk=request.data['id'])

    def delete(self, request, *args, **kwargs):
        qs = Project.objects.get(pk=request.data['id'])
        if qs:
            qs.delete()
            return Response({'status': 'success', 'msg': f"Project with {request.data['id']} id Deleted Successfully."})
        # serializer = ProjectSerializer(qs)
        return Response({'status': 'fail', 'msg': f"Project with {request.data['id']} id Deletion Failed."})


"""
extra gyan:
APIView vs Generic.APIView
|-> APIView is a base class. It doesn't assume much and will allow you to plug pretty much anything to it.
|-> GenericAPIView is meant to work with Django's Models. It doesn't assume much beyond all the bells and whistles the Model introspection can provide.
"""