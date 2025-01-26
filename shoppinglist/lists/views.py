from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import ListCategory, ListIndividual, Item
from .serializers import (
    ListCategorySerializer,
    ListIndividualSerializer,
    ItemSerializer,
)
from .permissions import IsOwnerOrReadOnly


class IndividualLists(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        shoppinglists = ListIndividual.objects.all()
        serializer = ListIndividualSerializer(shoppinglists, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = ListIndividualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(list_owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            shoppinglist = ListIndividual.objects.get(pk=pk)
            self.check_object_permissions(self.request, shoppinglist)
            return shoppinglist
        except ListIndividual.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        shoppinglist = self.get_object(pk)
        serializer = ListIndividualSerializer(shoppinglist)
        return Response(serializer.data)

    def put(self, request, pk):
        shoppinglist = self.get_object(pk)
        serializer = ListIndividualSerializer(
            instance=shoppinglist, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndividualCategory(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        listcategory = ListCategory.objects.all()
        serializer = ListCategorySerializer(listcategory, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = ListCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category_owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class CategoryDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            listcategory = ListCategory.objects.get(pk=pk)
            self.check_object_permissions(self.request, listcategory)
            return listcategory
        except ListCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        listcategory = self.get_object(pk)
        serializer = ListCategorySerializer(listcategory)
        return Response(serializer.data)

    def put(self, request, pk):
        listcategory = self.get_object(pk)
        serializer = ListCategorySerializer(
            instance=listcategory, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
