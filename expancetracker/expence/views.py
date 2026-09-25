from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from expence.serializer import UserSerializer,ExpenceSerializer
from django.contrib.auth.models import User
from expence.models import Expences
from rest_framework import status 
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Sum,Avg
from django.utils import timezone

# Create your views here.
class Signupview(ViewSet):
    def create(self,request):
        dserializer = UserSerializer(data=request.data)
        if dserializer.is_valid():
            User.objects.create_user(**dserializer.validated_data)
            return Response(data=dserializer.data,status=status.HTTP_201_CREATED)
        return Response(data=dserializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class ExpenceView(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request):
        dserializer = ExpenceSerializer(data=request.data)
        if dserializer.is_valid():
            dserializer.save(owner = request.user)
            return Response(data=dserializer.data,status=status.HTTP_201_CREATED)
        return Response(data=dserializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        expence_list = Expences.objects.filter(owner=request.user)
        ser = ExpenceSerializer(expence_list,many=True)
        return Response(data=ser.data,status=status.HTTP_200_OK)
    
    def destroy(self, request,pk=0):
        Expences.objects.get(id=pk).delete()
        return Response(data={"msg":"DELETED"})
    
    def update(self, request,pk=0):
        expence_obj = Expences.objects.get(id=pk)
        dser = ExpenceSerializer(data = request.data,instance=expence_obj)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request,pk=0):
        expence = Expences.objects.get(id=pk)
        dser = ExpenceSerializer(data = request.data,instance= expence,partial = True)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
            
class ExpenceSummary(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur_date = timezone.now()
        #print(cur_date)
        cur_month = cur_date.month
        cur_year = cur_date.year
        qs = Expences.objects.filter(owner = request.user,created_at__month=cur_month,created_at__year = cur_year).values('category').annotate(Sum('amount'))
        category_summary = [summary for summary in qs]
        for i in qs:
            print(i)
        total_expence = Expences.objects.filter(owner = request.user,created_at__month=cur_month,created_at__year = cur_year).values('amount').aggregate(Sum('amount'))
        #print(total_expence)
        context = {
            "total_expence":total_expence,
            "Category_summary":category_summary
        }
        return Response(data=context)
    
