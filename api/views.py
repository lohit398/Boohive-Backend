from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import UserSerializer
from base.models import Customer,Book
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime  

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        email = request.data['email'];
        pwd = request.data['password'];

        customer = Customer.objects.filter(email=email).first()

        if customer is None:
            raise AuthenticationFailed('User not found.')
        if not customer.check_password(pwd):
            raise AuthenticationFailed('Incorrect Password')
        data = {
            'id':customer.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(data,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key="token",value=token,httponly=True)
        return response

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('token')
        response.data = {'message':"successfully logged out."}
        return response

@api_view(['GET'])
def getBooks(request):
    books = Book.objects.all()
    books_list = list(books.values())
    return JsonResponse(books_list, safe=False)

@api_view(['POST'])
def reserveBook(request):
    pass


