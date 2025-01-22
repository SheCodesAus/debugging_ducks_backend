from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import ListCategory, ListIndividual
from .serializers import ListCategorySerializer, ListIndividualSerializer
from .permissions import IsOwnerOrReadOnly


class IndividualLists(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            shoppinglist = ListIndividual.objects.get(pk=pk)
            self.check_object_permissions(self.request, shoppinglist)
            return shoppinglist
        except ListIndividual.DoesNotExist:
            raise Http404
    
    def get(self, request, pk=None):
        if pk:
            # Fetch and return a single ListIndividual
            shoppinglist = self.get_object(pk)
            serializer = ListIndividualSerializer(shoppinglist)
            return Response(serializer.data)
        else:
            # Fetch and return all ListIndividual objects
            shoppinglists = ListIndividual.objects.all()
            serializer = ListIndividualSerializer(shoppinglists, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ListIndividualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(list_owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    def put(self, request, pk):
        shoppinglist = self.get_object(pk)
        serializer = ListIndividualSerializer(
            instance=shoppinglist,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        shoppinglist = self.get_object(pk)
        shoppinglist.delete()
        return Response(
            {"message": "Shopping list deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class ListCategory(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            listcategory = ListCategory.objects.get(pk=pk)
            self.check_object_permissions(self.request, categorylist)
            return listcategory
        except ListIndividual.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        # Fetch and return a lists Category
        listcategory = self.get_object(pk)
        serializer = ListCategorySerializer(listcategory)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ListCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(list_owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    def put(self, request, pk):
        listcategory = self.get_object(pk)
        serializer = ListCategorySerializer(
            instance=listcategory,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        listcategory = self.get_object(pk)
        listcategory.delete()
        return Response(
            {"message": "List Category deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    