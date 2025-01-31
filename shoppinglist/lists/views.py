from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
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
from datetime import datetime


class ItemsList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Item.objects.all()
        list_id = self.request.query_params.get('list_id', None)
        archived = self.request.query_params.get('archived', None)

        if list_id is not None:
            queryset = queryset.filter(list_id=list_id)
        
        if archived is not None:
            # Convert string 'false' to boolean False
            is_archived = archived.lower() == 'true'
            if is_archived:
                queryset = queryset.filter(archived_at__isnull=False)
            else:
                queryset = queryset.filter(archived_at__isnull=True)

        return queryset

    def get(self, request):
        items = self.get_queryset()
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

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=["list_id", "ranking"],
                message="This list already has an item with this ranking. Please choose a different ranking value.",
            )
        ]


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

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=["list_id", "ranking"],
                message="This list already has an item with this ranking. Please choose a different ranking value.",
            )
        ]


class ItemBulkUpdate(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request):
        # Request body should be a list of dictionaries, each containing item id and fields to update
        data = request.data
        ids = [item.get("id") for item in data]

        # Check if there are item IDs in the request data
        if not ids:
            return Response(
                {"detail": "No items provided to be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter for only the items to update
        items = Item.objects.filter(id__in=ids)

        # Create a map to quickly find items by their ID
        items_map = {item.id: item for item in items}

        # Loop through each update request and apply changes
        updated_items = []

        for item in data:
            updated_item = items_map.get(item["id"])
            if updated_item:
                # Update fields based on request data
                for field, value in item.items():
                    if field != "id":  # Don't update the 'id' field
                        setattr(updated_item, field, value)
                setattr(updated_item, "modified_at", datetime.now())
                setattr(updated_item, "modified_by", request.user)
                updated_items.append(updated_item)
            else:
                return Response(
                    {"detail": f"Product with id {item['id']} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Perform the bulk update
        Item.objects.bulk_update(
            updated_items,
            fields=[
                "name",
                "store",
                "link",
                "image",
                "ranking",
                "favourite",
                "purchased",
                "cost",
                "comments",
                "modified_at",
                "modified_by",
                "archived_at",
                "archived_by",
            ],
        )

        # Serialize the updated items
        serializer = ItemSerializer(updated_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
