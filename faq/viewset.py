from rest_framework.viewsets import ModelViewSet
from .models import Categories, FAQ, Customer
from .serializers import CategoriesSerializer, FAQSerializer, CustomerSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt as csfrf_exempt


class CategoriesViewSet(ModelViewSet):
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Categories.objects.all()


    
class FAQViewSet(ModelViewSet):
    serializer_class= FAQSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        return FAQ.objects.all()
    

    def destroy(self):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": f"FAQ '{instance.question}' deleted successfully."}, status=status.HTTP_200_OK)
    


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = []  

    def get_queryset(self):
        return Customer.objects.all()
    

    @csfrf_exempt
    @action(detail=False ,methods=['post'], permission_classes=[AllowAny])
    def customer_login(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)


        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        },
          status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def customer_logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token or token expired."}, status=status.HTTP_400_BAD_REQUEST)