from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import UserSerializer
from base.models import Customer,Book,Timeslot
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
            'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(data,'secret',algorithm='HS256')
        
        response = Response({
            'token' : token
        })
        return response

def validateJwt(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Bearer'):
        raise AuthenticationFailed('Unauthenticated Request')
    token = auth_header.split(" ")[1]
    if not token:
        raise AuthenticationFailed('Unauthenticated Request')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except:
        raise AuthenticationFailed('Invalid token')
    customer = Customer.objects.filter(id=payload['id']).first()
    if not customer:
        return False
    return True

@api_view(['GET'])
def getBooks(request):
    if not validateJwt(request):
        raise AuthenticationFailed('Unauthenticated Request')
    books = Book.objects.all()
    books_list = list(books.values())
    return JsonResponse(books_list, safe=False)


def availability_helper(request):
    today = datetime.date.today()
    start_date = datetime.date(today.year,today.month,1)
    end_date = start_date + datetime.timedelta(days=90)
    availability = {}
    i = 0
    while i<=90:
        availability[(start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")] = True
        i+=1
    query ="""
    SELECT * FROM base_timeslot t WHERE ((t.start <= %s AND t.end >= %s) 
    OR (t.start >= %s AND t.end <= %s) 
    OR  (t.start <= %s AND t.end >= %s)) AND t.book_id = %s
    """
    timeslots = Timeslot.objects.raw(query,(start_date,start_date,start_date,end_date,end_date,end_date,request.data['book']))
    for booking in timeslots:
        start = booking.start-datetime.timedelta(days=1)
        end = booking.end-datetime.timedelta(days=1)
        i = 0
        curr = start 
        while curr <= end:
            availability[curr.strftime("%Y-%m-%d")] = False
            curr+=datetime.timedelta(days=1)
    return availability

@api_view(['GET'])
def checkAvailability(request):
    if not validateJwt(request):
        raise AuthenticationFailed('Unauthenticated Request')
    availability = availability_helper(request)
    return JsonResponse(availability, safe=False)

    
    


