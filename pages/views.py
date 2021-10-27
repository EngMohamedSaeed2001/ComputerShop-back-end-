import os

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from pages.Serializers.AdminSerializers import *
from pages.Serializers.ClientSerializer import *
from .models import *
from .permissions import IsStaff
from .render import UserRenderer


# //////////// REGISTERATION ////////////////////

# Register API


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class SignUp(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        if user.email.__contains__('@admin.com'):
            user.is_staff = True
            user.save()
        # Verify
        '''
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email_verify')
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
            email_body = 'Hi ' + user.username + \
                         ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email', 'me': 'engmohamedsaeed19@gmail.com', 'pass': '2001019678380919'}
        
        Util.sendEmail(data)
        '''

        return Response({'user': user_data, }, status=status.HTTP_201_CREATED)

    # Untill finish front-end (Verify)
    '''
    class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    '''


class ResetPassword(generics.GenericAPIView):
    serializer_class = UserSerializer
    permissions_class = permissions.IsAuthenticated

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        client = Client.objects.get(id=user.id)
        client.password = request.data['new_password']
        client.save()
        return Response({
            'message': 'Password is updated successfully !!',

        }, status=status.HTTP_201_CREATED)


class Logout(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        RefreshToken(token=refresh_token).blacklist()

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_204_NO_CONTENT)


# Social Login


# ////////////////// ADMIN ///////////////////
# Section

class AddSections(generics.GenericAPIView):
    serializer_class = AddSectionSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        section = serializer.save()
        return Response({
            "section": SectionsSerializer(section, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)


class Sections(generics.GenericAPIView):
    serializer_class = AddSectionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        sections = Section.objects.all()
        if sections:
            serializer = SectionsSerializer(sections, many=True)
            return Response(serializer.data)
        else:
            return Response('There are no sections yet ')


def getSection(sectionId):
    section = Section.objects.get(id=sectionId)
    return section


class GetSectionId(generics.GenericAPIView):
    serializer_class = AddSectionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, sectionId):
        sections = getSection(sectionId)
        if sections:
            serializer = SectionsSerializer(sections, many=False)
            return Response(serializer.data)
        else:
            return Response('Section doesnt exist')


class EditSection(generics.GenericAPIView):
    serializer_class = AddSectionSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def patch(self, request, sectionId):
        section = getSection(sectionId)
        serializer = SectionsSerializer(section, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Section updated successfully !!',
            "section": serializer.data,
        }, status=status.HTTP_201_CREATED)


class DeleteSection(generics.GenericAPIView):
    serializer_class = AddSectionSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def delete(self, request, sectionId):
        section = get_object_or_404(Section, id=sectionId)
        section.delete()

        return Response({'message': 'Deleted successfully!!'}, status=status.HTTP_200_OK)


# //////////////////////////////////

# Product
if permissions.IsAuthenticated:
    def oldToNew():
        product = Product.objects.all().filter(status='new')

        currentDay = datetime.date.today().day
        currentMonth = datetime.date.today().month
        currentTime = datetime.datetime.now().time().second

        for obj in product.iterator():
            proDay = obj.date.day
            proMonth = obj.date.month
            proTime = obj.date.time().second
            if (currentDay == proDay) and (currentMonth != proMonth) and (currentTime != proTime):
                obj.status = 'old'
                obj.save()


class AddProducts(generics.GenericAPIView):
    serializer_class = AddProductSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response({
            "product": ProductsSerializer(product, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)


class Products(generics.GenericAPIView):
    serializer_class = AddProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        oldToNew()
        products = Product.objects.all().order_by('price')
        if products:
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response('No products yet')


def getProduct(productId):
    product = Product.objects.get(id=productId)

    return product


class GetProductId(generics.GenericAPIView):
    serializer_class = AddProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, productId):
        products = getProduct(productId)
        if products:
            serializer = ProductsSerializer(products, many=False)
            return Response(serializer.data)
        else:
            return Response('Product doesnt exist')


class NewProducts(generics.GenericAPIView):
    serializer_class = AddProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        oldToNew()

        products = Product.objects.all().filter(status='new').order_by('price')
        if products:
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response('No new products')


class OldProducts(generics.GenericAPIView):
    serializer_class = AddProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        oldToNew()
        products = Product.objects.all().filter(status='old').order_by('price')
        if products:
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response('No old products')


class EditProduct(generics.GenericAPIView):
    serializer_class = AddProductSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def patch(self, request, productId):
        product = getProduct(productId)
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Product updated successfully !!',
            "product": serializer.data,
        }, status=status.HTTP_201_CREATED)


class DeleteProduct(generics.GenericAPIView):
    serializer_class = AddProductSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def delete(self, request, productId):
        product = get_object_or_404(Product, id=productId)
        product.delete()

        return Response({'message': 'Deleted successfully!!'}, status=status.HTTP_200_OK)


# ////////////////////////////

# Offer
class AddOffers(generics.GenericAPIView):
    serializer_class = AddOfferSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer = serializer.save()
        return Response({
            "offer": OfferSerializer(offer, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)


def getOffer(offerId):
    offer = Offer.objects.get(id=offerId)
    return offer


class GetOfferId(generics.GenericAPIView):
    serializer_class = AddOfferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, offerId):
        offers = getOffer(offerId)
        if offers:
            serializer = OfferSerializer(offers, many=False)
            return Response(serializer.data)
        else:
            return Response('Offer doesnt exist')


class EditOffer(generics.GenericAPIView):
    serializer_class = AddOfferSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def patch(self, request, offerId):
        offer = getOffer(offerId)
        serializer = OfferSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Offer updated successfully !!',
            "Offer": serializer.data,
        }, status=status.HTTP_201_CREATED)


class DeleteOffer(generics.GenericAPIView):
    serializer_class = AddOfferSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def delete(self, request, offerId):
        offer = get_object_or_404(Offer, id=offerId)
        offer.delete()

        return Response({'message': 'Deleted successfully!!'}, status=status.HTTP_200_OK)


class Offers(generics.GenericAPIView):
    serializer_class = AddOfferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        offers = Offer.objects.all()
        if offers:
            serializer = OfferSerializer(offers, many=True)
            return Response(serializer.data)
        else:
            return Response('No offers yet')


# ////////////////////////////

# ////////////////////// CLIENT /////////////////

class Clients(generics.GenericAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        if clients:
            return Response(serializer.data)
        else:
            return Response('No clients yet')

    def post(self, request):
        obj = ClientSerializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response(obj.data, status=status.HTTP_201_CREATED)
        return Response(obj.errors, status=status.HTTP_404_NOT_FOUND)


class CurrentUser(generics.GenericAPIView):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = ClientSerializer(user)
        data = {
            'username': serializer.data['username'],
            'email': serializer.data['email'],
            'order': serializer.data['order'],
            'fav': serializer.data['fav']
        }
        return Response(data)


class UserById(generics.GenericAPIView):
    def get(self, request, userId):
        user = Client.objects.get(id=userId)
        if user:
            serializer = ClientSerializer(user)
            data = {
                'username': serializer.data['username'],
                'email': serializer.data['email'],
                'order': serializer.data['order'],
                'fav': serializer.data['fav']
            }
            return Response(data)
        else:
            return Response('User doesnt exist')


# favourite

class AddFav(generics.GenericAPIView):
    serializer_class = AddFavSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fav = serializer.save()
        return Response({
            "fav": FavSerializer(fav, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)


def getFav(favId):
    fav = Favourite.objects.get(id=favId)
    return fav


class GetFavId(generics.GenericAPIView):
    serializer_class = AddFavSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, favId):
        favs = getFav(favId)
        if favs:
            serializer = FavSerializer(favs, many=False)
            return Response(serializer.data)
        else:
            return Response('Favourite doesnt exist')


class EditFav(generics.GenericAPIView):
    serializer_class = AddFavSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, favId):
        fav = getFav(favId)
        serializer = FavSerializer(fav, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Favourite updated successfully !!',
            "Favourite": serializer.data,
        }, status=status.HTTP_201_CREATED)


class DeleteFav(generics.GenericAPIView):
    serializer_class = AddFavSerializer
    permissions_classes = permissions.IsAuthenticated

    def delete(self, request, favId):
        fav = get_object_or_404(Favourite, id=favId)
        fav.delete()

        return Response({'message': 'Deleted successfully!!'}, status=status.HTTP_200_OK)


class Fav(generics.GenericAPIView):
    serializer_class = AddFavSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        fav = Favourite.objects.all()
        if fav:
            serializer = FavSerializer(fav, many=True)
            return Response(serializer.data)
        else:
            return Response('No favourite yet')


# Order

class AddOrder(generics.GenericAPIView):
    serializer_class = AddOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({
            "order": OrderSerializer(order, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)


def getOrder(orderId):
    order = Order.objects.get(id=orderId)
    return order


class GetOrderId(generics.GenericAPIView):
    serializer_class = AddOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, orderId):
        orders = getOrder(orderId)
        if orders:
            serializer = OrderSerializer(orders, many=False)
            return Response(serializer.data)
        else:
            return Response('Order doesnt exist')


class EditOrder(generics.GenericAPIView):
    serializer_class = AddOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, orderId):
        order = getOrder(orderId)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Order updated successfully !!',
            "Order": serializer.data,
        }, status=status.HTTP_201_CREATED)


class DeleteOrder(generics.GenericAPIView):
    serializer_class = AddOrderSerializer
    permissions_classes = permissions.IsAuthenticated

    def delete(self, request, orderId):
        order = get_object_or_404(Order, id=orderId)
        order.delete()

        return Response({'message': 'Deleted successfully!!'}, status=status.HTTP_200_OK)


class Orders(generics.GenericAPIView):
    serializer_class = AddOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        order = Order.objects.all()
        if order:
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        else:
            return Response('No orders yet')


# Filtration

class FilterByPrice(generics.GenericAPIView):
    permissions_classes = permissions.IsAuthenticated

    def get(self, request):
        products = Product.objects.all()

        search = products.filter(price=float(request.data['price'])).order_by('price')
        if search:
            for query in search.iterator():
                return Response({
                    'name': query.name,
                    'price': query.price,
                    'description': query.description,
                    'image': str(query.image)
                })

        else:
            return Response('Product doesnt exist')


class FilterByName(generics.GenericAPIView):
    permissions_classes = permissions.IsAuthenticated

    def get(self, request):
        products = Product.objects.all()

        query = products.filter(name__contains=request.data['name']).order_by('price')
        if query:

            return Response({
                'name': query.get().name,
                'price': query.get().price,
                'description': query.get().description,
                'image': str(query.get().image)
            })

        else:
            return Response('Product doesnt exist')


class FilterByPriceAndName(generics.GenericAPIView):
    permissions_classes = permissions.IsAuthenticated

    def get(self, request):
        products = Product.objects.all()

        query = products.filter(name__contains=request.data['name'], price=float(request.data['price'])).order_by(
            'name', 'price')
        if query:

            return Response({
                'name': query.get().name,
                'price': query.get().price,
                'description': query.get().description,
                'image': str(query.get().image)
            })

        else:
            return Response('Product doesnt exist')

# //////////////////////////////////////////////////////////////////////////

# Payment Method
