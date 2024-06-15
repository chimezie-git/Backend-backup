from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

class TemiiWebhook(GenericAPIView):
    def post(self, request, *args, **kwargs):
        pass