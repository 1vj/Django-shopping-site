from django.shortcuts import render,redirect,get_object_or_404
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import User,item,cart,wishlist
from rest_framework.response import Response
from .serializer import UserSerializer,itemSerializer,cartSerializer
from .email_token import generate_email_auth_token
import uuid
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens  import RefreshToken 
from rest_framework import status
from rest_framework.permissions import AllowAny
import datetime
from .authentication import SafeJWTAuthentication
import requests
from rest_framework import exceptions
from .tokenOps import generate_tokens
import jwt
from rest_framework.exceptions import AuthenticationFailed, ParseError

# Create your views here.
class register(APIView):
    def post(self,request):
        name = request.data["name"]
        email = request.data["email"]
        username =request.data["username"]
        password = request.data["password"]
        user = User.objects.filter(email = email)
        if user.exists() or User.objects.filter(username = username).first():
            return Response({'msg':'user already exists'})
        else:
            user = User(name = name,email=email, username=username,password= password)
            # jwt_payload = {'email': user.email}
            # jwt_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm='HS256')

            

            device_uuid = uuid.uuid4()  # Generate a random UUID for the device
            email_auth_token = generate_email_auth_token(device_uuid)
            print(type(email_auth_token))
            user.auth_token = email_auth_token
            print(email_auth_token)
            subject = "Verify account"
            message = f"Welcome {name}! \n Please verify your account to activate.\n\n\n\n\n \n https://9caa-115-246-125-172.ngrok-free.app /verify/{email_auth_token}/"
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [email,]
            send_mail(subject,message,email_from,recepient_list)
            # fm.save() 
            
            user.save()
        return Response({'msg':'data inserted'})

class login(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        email = request.data["email"]
        print(email)
        password = request.data["password"]
        print(password)
        user = User.objects.filter(email=email).first()
        
        print(user)
        if not user:
            return Response({'msg': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.email ==email and user.password ==password:
            jwt_token = generate_tokens(user)
            if user.is_authenticated == True:
                if user.is_admin ==True:
                    return Response({'msg': 'Admin logged in successfully'},status=status.HTTP_200_OK)
                else:
                    cart_item = user.cart_item
                    print(cart_item)
                    if cart_item != None:
                        total_items = sum(item['quantity'] for item in cart_item)
                    else:
                        total_items = 0
                    print(total_items)
                    print("printing the access token from login", jwt_token["access"])
                    return Response({'msg': 'User logged in successfully','user':user.username,'cart_total':total_items,'token':jwt_token},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'verify email first'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'msg':'invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)

        # if user.is_authenticated == True:
        #     if user.password == password:
        #         if user.is_admin:
        #             return Response({'msg': 'Admin logged in successfully and item saved'})
        #         else:
        #             return Response({'msg': 'User logged in successfully'})
        #     else:
        #         return Response({'msg': 'Invalid password. Please try again.'})

           
class add_item(APIView):
    def post(self,request,username):
        user = User.objects.filter(username=username).first()
        if user.is_admin:
            brand_name = request.data["brand_name"]
            item_name = request.data["item_name"]
            desc = request.data["desc"]
            discounted_price =request.data["discounted_price"] 
            available_number = request.data["available_number"]
            item_image =request.data["image"]
            actual_price = request.data["actual_price"]
            print("This is image",item_image)
            print(request.FILES)
            # print(request.FILES['image'])
            response = request.FILES['image']
            print(response)
            
            # print(response)
            # print(response)
            
            print("imageee ")
            file_name = response
            print(file_name)

            
            item_add = item(brand_name = brand_name,item_name = item_name,desc = desc,discounted_price = discounted_price,actual_price = actual_price,available_number = available_number)
            item_add.image.save(file_name.name,response, save=True)
            item_add.save()
            return Response({'msg':'item added successfully'})
        else:
            return Response({'msg':'can not add this item'})
        
    def put(self,request,username):
        user = User.objects.filter(username=username).first()
        item_name = request.data["item_name"]
        if user.is_admin:
            item_obj = item.objects.filter(item_name = item_name).first()
            if item_obj:
                Serializer = itemSerializer(item_obj,request.data,partial=True)
                if Serializer.is_valid():
                        Serializer.save()
                        return Response({'msg':'Updated the data'})
                
            else:
                return Response({'msg':'item doesnt exist'})
        else:
            return Response({'msg':'unable to update'})
        
    def delete(self,request,username):
        user = User.objects.filter(username=username).first()
        delete_item = request.data["item_name"]
        if(user):
            item_record = item.objects.filter(item_name=delete_item)
            item_record.delete()
        return Response({'msg':'record deleted successfully'})
    
class addCart(APIView):

    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, username):
        print("cart")
        authorization_header = request.headers.get('Authorization')
        print(authorization_header)
        user = User.objects.filter(username=username).first()
        
        if user:
            print("user exist")
            item_name = request.data.get("item_name")
            item_available = item.objects.filter(item_name=item_name).first()

            if item_available.available_number > 0:
                print("HEYAAAAA")
                # Create or retrieve the user's cart
                try:
                    cart_obj = cart.objects.get(user=user)
                except:
                    cart_obj = cart.objects.create(user=user)
                
                cart_items = user.cart_item or []  # Retrieve cart items, or initialize an empty list
                item_already_in_cart = False
                print(cart_items)
                # Check if the item is already in the cart
                for cart_item in cart_items:
                    if cart_item['item'] == item_name:
                        # If the item is already in the cart, increment its quantity
                        cart_item['quantity'] += 1
                        item_already_in_cart = True
                        break
                
                if not item_already_in_cart:
                    # If the item is not in the cart, add it with quantity 1
                    new_cart_item = {
                        'item': item_name,
                        'quantity': 1
                    }
                    cart_items.append(new_cart_item)
                
                user.cart_item = cart_items
                
                # Add the item to the cart
                cart_obj.product.add(item_available)
                
                # Calculate the total discounted_price (assuming item discounted_price is available)
                cart_obj.total_discounted_price += item_available.discounted_price
                
                user.cart_value = cart_obj.total_discounted_price
                
                # Decrease the available number of the item by 1
                # item_available.available_number -= 1
                
                # Save the changes
                cart_obj.save()
                item_available.save()
                user.save()
                
                return Response({'msg': 'Item added to cart successfully'})
            else:
                return Response({'msg': 'Item is not available or out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'User not found'}, status=404)
        
class buyNow(APIView):
    def post(self,request,username):
        print(username)
        user = User.objects.filter(username=username).first()
        if user:
            if user.is_admin == False:
                order  = user.cart_item
                user.order = order
                print("USEr order",user.order)
                for i in user.order:
                    print("feeling something")
                    print("item",i)
                    item_obj = item.objects.filter(item_name = i["item"]).first()
                    if item_obj.available_number >0:
                        item_obj.available_number -= i["quantity"]
                        item_obj.save()
                        
                    else:
                        user.order = user.order.remove(i)
                        print("after removing",user.order)
                        user.cart_value -= item_obj.actual_price
                        print("cart value",user.cart_value)
                        # return Response({'msg':'item out of stock '})
                    print(item_obj.available_number)
                user.order_value = user.cart_value
                user.cart_value = 0
                user.cart_item = []
                cart_obj = cart.objects.filter(user=user).first()
                user.save()
                if cart_obj:
                    cart_obj.delete()
                return Response({'msg': 'Order placed'}, status=status.HTTP_200_OK)
                #cart_obj.save()
        else:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)        
                

class showItem(APIView):
    def get(self,request):
        products = item.objects.all()
        serializer = itemSerializer(products,many=True)
        return Response(serializer.data,content_type='application/json')

class verify(APIView):
    def get(self,request,token):
        try:
            user = User.objects.filter(auth_token = token).first()
            user.is_authenticated = True
            user.save()
            return Response({'msg':'user authenticated and now able to login'})
        except:
            return Response({'msg':'user not authenticated'})
        
class showCart(APIView):
    def get(self,request,username):
        user_obj = User.objects.filter(username = username).first()
        cart_obj = cart.objects.filter(user = user_obj)
        serialized_data = cartSerializer(cart_obj , many = True)
        return Response(serialized_data.data)
    



        
class showCart_2(APIView):
    def get(self, request, username):
        user_obj = User.objects.filter(username=username).first()
        cart_items_data = []
        for item_entry in user_obj.cart_item:
            item_data = item.objects.filter(item_name=item_entry["item"]).first()
            serialized_data = itemSerializer(item_data).data
            
            # Update the serializer to include the new field
            serialized_data["quantity"] = item_entry["quantity"]
            cart_items_data.append(serialized_data)
        return Response({'cart_items': cart_items_data, 'msg': 'success'})

    
class wishlistAPI(APIView):
    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
            item_name = request.data.get("item_name")
            item_obj = item.objects.filter(item_name=item_name).first()

            if not item_obj:
                return Response({'msg': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

            wishlist_obj, created = wishlist.objects.get_or_create(user=user)
            wishlist_obj.product.add(item_obj)
            wishlisted_items = wishlist_obj.product.all()
            serializer = itemSerializer(wishlisted_items, many=True)
            return Response({'msg': 'Item wishlisted', 'wishlisted_items': serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class removeCartAPI(APIView):
    def post(self,request,username):
        print("In the loop")
        item_name = request.data.get('item_name')
        user = User.objects.filter(username=username).first()
        cart_obj = cart.objects.filter(user = user).first()
        # cart_obj.product.remove(item_name)
        for i in user.cart_item:
            if i["item"] ==item_name:
                user.cart_item.remove(i)
                item_obj = get_object_or_404(item, item_name=item_name)
                quantity = i["quantity"]
                discounted_price = item_obj.discounted_price
                    
                    # Update the total_discounted_price of the cart
                cart_obj.total_discounted_price -= (discounted_price * quantity)
                user.cart_value -=(discounted_price *quantity)
                
                cart_obj.product.remove(item_obj)

            # cart_obj = cart_obj.
        user.save()
        cart_obj.save()
        return Response({'msg':'item removed from cart'}) 

class removeOne(APIView):
    def post(self,request,username):
        print("In the loop")
        item_name = request.data.get('item_name')
        user = User.objects.filter(username=username).first()
        cart_obj = cart.objects.filter(user = user).first()
        # cart_obj.product.remove(item_name)
        for i in user.cart_item:
            if i["item"] ==item_name:
                # user.cart_item.remove(i)
                i["quantity"] -= 1
                item_obj = get_object_or_404(item, item_name=item_name)
                quantity = i["quantity"]
                discounted_price = item_obj.discounted_price
                    
                    # Update the total_discounted_price of the cart
                cart_obj.total_discounted_price -= (discounted_price)
                user.cart_value -=(discounted_price)
                
                cart_obj.product.remove(item_obj)

            # cart_obj = cart_obj.
        user.save()
        cart_obj.save()
        return Response({'msg':'item removed from cart'}) 

class showWishlist(APIView):
    def get(self, request,username):
        user = User.objects.get(username=username)
        wishlist_obj, created = wishlist.objects.get_or_create(user=user)
        # wishlist_obj.product.add(item_obj)
        wishlisted_items = wishlist_obj.product.all()
        serializer = itemSerializer(wishlisted_items, many=True)
        return Response({'msg': 'Item wishlisted', 'wishlisted_items': serializer.data}, status=status.HTTP_200_OK)

class refresh_token_View(APIView):
    def post(self,request):
        refresh_token = request.data.get('refresh_token')
        print(refresh_token)  # Assuming refresh token is sent in the request data
        if refresh_token is None:
            raise AuthenticationFailed('Refresh token is missing.')

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Expired refresh token. Please login again.')

        user = User.objects.filter(username=payload['user_id']).first()
        if user is None:
            raise AuthenticationFailed('User not found.')

        # if not user.is_active:
        #     raise AuthenticationFailed('User is inactive.')

        access_token = generate_tokens(user)
        print(access_token)  # Assuming you have a function to generate access tokens
        return Response({'access_token': access_token})


        

        


