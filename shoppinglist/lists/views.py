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
    CategoryDetailSerializer,
    ListDetailSerializer,
    ItemDetailSerializer,
)
from .permissions import IsOwnerOrReadOnly


class ItemsList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            item = Item.objects.get(pk=pk)
            self.check_object_permissions(self.request, item)
            return item
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemDetailSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemDetailSerializer(
            instance=item, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(modified_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ListsFromLoggedInUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        shoppinglists = ListIndividual.objects.filter(list_owner=request.user)
        serializer = ListIndividualSerializer(shoppinglists, many=True)
        return Response(serializer.data)


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
        serializer = ListDetailSerializer(shoppinglist)
        return Response(serializer.data)

    def put(self, request, pk):
        shoppinglist = self.get_object(pk)
        serializer = ListDetailSerializer(
            instance=shoppinglist, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(modified_by=request.user)
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


class CategoriesFromLoggedInUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        listcategory = ListCategory.objects.filter(category_owner=request.user)
        serializer = ListCategorySerializer(listcategory, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            listcategory = ListCategory.objects.get(pk=pk)
            self.check_object_permissions(self.request, listcategory)
            return listcategory
        except ListCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        listcategory = self.get_object(pk)
        serializer = CategoryDetailSerializer(listcategory)
        return Response(serializer.data)

    def put(self, request, pk):
        listcategory = self.get_object(pk)
        serializer = CategoryDetailSerializer(
            instance=listcategory, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(modified_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
