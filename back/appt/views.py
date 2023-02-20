from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Treatment, Customer, Bday_benefit, Appointment, Product, Image
from .serializers import TreatmentSerializer, CustomerSerializer, AppointmentSerializer, ProductSerializer, ImageSerializer
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


# <!-- Code after Omer's practice session: -->
# @api_view(["POST"])
# def fileUploadView(request):
#     file_obj= request.FILES["photo"]
#     file_model= Image(title="myImage", imgae=file_obj)
#     file_model.save()
#     file_path = default_storage.save('media/Posted_Images' + str(file_model.image), ContentFile(file_obj.read()))
#     print(file_path)
#     return Response({"success": False, "error": "File upload failed"}, status=400)

# Improved code from GPT that explained that the above code will always return a fialure because of the success: false:
# @api_view(["POST"])
# def fileUploadView(request):
#     try:
#         file_obj = request.FILES["photo"]
#         file_model = Image(title="myImage", image=file_obj)
#         file_model.save()
#         file_path = default_storage.save('media/Posted_Images' + str(file_model.image), ContentFile(file_obj.read()))
#         return Response({"success": True, "file_path": file_path})
#     except Exception as e:
#         return Response({"success": False, "error": str(e)}, status=400)

#Improved improved GPT code so the posted image folder be created only once: fron the 20.02.2023:
# @api_view(["POST"])
# def fileUploadView(request):
#     try:
#         file_obj = request.FILES["photo"]
#         file_model = Image(title="myImage", image=file_obj)
#         file_model.save()
#         file_path = default_storage.save('media/Posted_Images/' + str(file_model.image), ContentFile(file_obj.read()))
#         return Response({"success": True, "file_path": file_path})
#     except Exception as e:
#         return Response({"success": False, "error": str(e)}, status=400)

#Improved improved GPT code so the posted image folder be created only once: fron the 20.02.2023 09:31:
# @api_view(["POST"])
# def fileUploadView(request):
#     try:
#         file_obj = request.FILES["photo"]
#         file_model = Image(title="myImage", image=file_obj)
#         file_model.save()

#         directory = 'media/Posted_Images/'
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#         file_path = default_storage.save(directory + str(file_model.image), ContentFile(file_obj.read()))
#         return Response({"success": True, "file_path": file_path})
#     except Exception as e:
#         return Response({"success": False, "error": str(e)}, status=400)
#Improved improved GPT code so the posted image folder be created only once: fron the 20.02.2023 09:45:
@api_view(["POST"])
def fileUploadView(request):
    try:
        file_obj = request.FILES["photo"]
        file_model = Image(title="myImage")
        file_model.save()

        directory = 'media/Posted_Images/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = str(file_model.id) + '_' + file_obj.name
        file_path = default_storage.save(directory + file_name, ContentFile(file_obj.read()))
        file_model.image = file_path
        file_model.save()
        
        return Response({"success": True, "file_path": file_path})
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=400)

# ////////////////////////////////login /register
# login
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims
#         token['username'] = user.username
#         token['email'] = user.email
#         token['is_admin'] = user.is_superuser
#         return token


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

##Liron thinks of changing the login to the following: (because saying logged in when not registered yet)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        if user.is_authenticated:
            token['username'] = user.username
            token['email'] = user.email
            token['is_admin'] = user.is_superuser
        else:
            raise AuthenticationFailed("User is not authenticated.")
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


##Liron thinks of changing the login the above code

# register


@api_view(['POST'])
def register(req):
    username = req.data["username"]
    password = req.data["password"]
    # create a new user (encrypt password)
    try:
        User.objects.create_user(username=username, password=password)
    except:
        return Response("error")
    return Response(f"{username} registered")

# logout


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def do_logout(request):
    logout(request)
    return Response({"detail": "logout"}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def getImages(request):
#     res=[] #create an empty list
#     for img in Customer.objects.all(): #run on every row in the table...
#         res.append({"customer_id":img.customer_id,
#                 "name":img.name,
#                 "p_number":img.p_number,
#                 "age":img.page,
#                "image":str(img.image)
#                 }) #append row by to row to res list
#     return Response(res) #return array as json response


###Liron added
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_images(request):
    """
    List of all product images.
    """
    res = []
    for img in Image.objects.all():  # run on every row in the table...
        res.append({
            "_id": img.id,
            "title": img.title,
            "image":str(img.image)
                    })  # append row by to row to res list
    return Response(res, safe=False)  # return array as json response
###Liron added


# class APIViews(APIView):
#     parser_class=(MultiPartParser,FormParser)
#     def get (self, request):
#         tasks = Customer.objects.all()
#         serializer = CustomerSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request,*args,**kwargs):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response (serializer.data, status=status.HTTP_201_CREATED)
#         return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##Liron added to compare (code from the shoe ecommerce)
# class ImageViews(APIView):
#     parser_class = (MultiPartParser, FormParser)
#     permission_classes = [IsAdminUser]
#     """
#     Add a new product image to DB.
#     """
#     def post(self, request, *args, **kwargs):
#         api_serializer = ImageSerializer(data=request.data)
#         if api_serializer.is_valid():  # the serializer check the data
#             api_serializer.save()  # save to DB (path,str) and save the actual file to directory
#             return Response(api_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print('error', api_serializer.errors)
#             return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class New_Customer(APIView):
    parser_class = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]

    def get(self, request):
        customers = request.user.customer_set.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        customers = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(customers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        customers = Customer.objects.get(pk=pk)
        customers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class TreatmentView(APIView):
    def get(self, request):
        my_model = Treatment.objects.all()
        serializer = TreatmentSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TreatmentSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        treatments = Treatment.objects.get(pk=pk)
        serializer = TreatmentSerializer(treatments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        treatments = Treatment.objects.get(pk=pk)
        treatments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class AppointmentView(APIView):
    def get(self, request):
        my_model = Appointment.objects.all()
        serializer = AppointmentSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        appointments = Appointment.objects.get(pk=pk)
        serializer = AppointmentSerializer(appointments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        appointments = Appointment.objects.get(pk=pk)
        appointments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class ProductView(APIView):

    def get(self, request):

        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = ProductSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        my_model = Product.objects.get(pk=pk)
        serializer = ProductSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        my_model = Product.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
