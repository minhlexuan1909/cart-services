from django.shortcuts import render

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from datetime import datetime


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.queryset.filter(account_id=self.request.user.id)

    def get_serializer_class(self):
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(account_id=self.request.user.id)

    def list(self, request):
        """Auto create when user has no cart"""
        print(self.queryset)
        if not self.queryset.exists():
            cart = Cart.objects.create(account_id=self.request.user.id)
            cart.cart_items = []
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        cart = self.queryset.first()
        cart.cart_items = CartItem.objects.filter(cart=cart)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()
