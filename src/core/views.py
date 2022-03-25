from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status  # User Register

from .serializers import RegisterSerializer, ProjectSerializer, Project, Task, TaskSerializer, Permission, PermissionSerializer
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


class RegisterView(generics.CreateAPIView):
    qs = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):  # somehow this is not working
        projid = self.request.query_params.get('id')
        print(projid)
        qs = Project.objects.get(pk=projid)
        serializer = ProjectSerializer(qs)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        qs = Project.objects.all()
        serializer = ProjectSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            qs = Project.objects.get(pk=request.data['id'])
            serializer = ProjectSerializer(data=request.data, instance=qs)
            """print(type(qs.created_by.id),
                  type(request.data['created_by']),
                  qs.created_by.id is request.data['created_by'])"""
            if qs.created_by.id == int(request.data['created_by']):
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': "success", 'data': serializer.data},
                                    status=status.HTTP_202_ACCEPTED)
                return Response({'status': 'error', 'data': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'error', "message": "unauthorized access."},
                            status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response({'status': 'error', 'message': 'project id is required for updating project.'},
                            status=status.HTTP_417_EXPECTATION_FAILED)

    def delete(self, request, *args, **kwargs):
        try:
            qs = Project.objects.get(pk=request.data['id'])
            if qs:
                qs.delete()
                return Response({'status': 'success',
                                 'msg': f"Project with {request.data['id']} id Deleted Successfully."},
                                status=status.HTTP_200_OK)
        except BaseException:
            return Response({'status': 'fail',
                             'msg': f"Project with {request.data['id']} id Not Found, Failed to Delete."},
                            status=status.HTTP_404_NOT_FOUND)


class TaskView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            qs = Project.objects.get(pk=request.data['id']).task_set.all()
            serializer = TaskSerializer(qs, many=True)
            return Response(serializer.data)
        except KeyError:
            return Response({'status': 'error', 'message': 'project id is required for getting tasks.'},
                            status=status.HTTP_417_EXPECTATION_FAILED)

    def post(self, request, *args, **kwargs):
        try:
            qs = Project.objects.get(pk=request.data['proj_id'])
            if qs.created_by.id == int(request.data['userid']):
                serializer = TaskSerializer(data=request.data)
                # print(request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'error',
                                 'message': "authorization error, this user doesn't have permission."},
                                status=status.HTTP_403_FORBIDDEN)
        except BaseException:
            return Response({'status': 'error', 'message': 'please provide proper proj_id or/and userid'},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            qs = Task.objects.get(pk=request.data['id'])
            serializer = TaskSerializer(data=request.data, instance=qs)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "success", 'data': serializer.data},
                                status=status.HTTP_202_ACCEPTED)
            return Response({'status': 'error', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'status': 'error', 'message': 'task id is required for updating task.'},
                            status=status.HTTP_417_EXPECTATION_FAILED)

    def delete(self, request, *args, **kwargs):
        try:
            qs = Task.objects.get(pk=request.data['id'])
            if qs:
                qs.delete()
                return Response({'status': 'success',
                                 'msg': f"Task with {request.data['id']} id Deleted Successfully."},
                                status=status.HTTP_200_OK)
        except BaseException:
            return Response({'status': 'fail',
                             'msg': f"Task with {request.data['id']} id Not Found, Failed to Delete."},
                            status=status.HTTP_404_NOT_FOUND)


class PermissionView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = PermissionSerializer(data=request.data)
        try:
            qs = Project.objects.get(pk=request.data['proj_id'])
            try:
                qs = User.objects.get(pk=request.data['user_id'])
            except BaseException:
                return Response({'status': "user id not found,"})
        except BaseException:
            return Response({'status': "project id not found,"})
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            qs = Permission.objects.get(pk=request.data['id'])
            if qs:
                qs.delete()
                return Response({'status': 'success',
                                 'msg': f"Task with {request.data['id']} id Deleted Successfully."},
                                status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'fail',
                             'msg': f"Task with {request.data['id']} id Not Found, Failed to Delete."},
                            status=status.HTTP_404_NOT_FOUND)

"""
extra gyan:
APIView vs Generic.APIView
|-> APIView is a base class. It doesn't assume much and will allow you to plug pretty much anything to it.
|-> GenericAPIView is meant to work with Django's Models. It doesn't assume much beyond all the bells and whistles the Model introspection can provide.
"""