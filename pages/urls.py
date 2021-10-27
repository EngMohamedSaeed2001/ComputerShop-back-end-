from django.urls import path

from .views import *

urlpatterns = [

    # ////// CLIENT //////

    path('computerShop/clients/', Clients.as_view(queryset=Client.objects.all()), name='clients'),
    path('computerShop/me/', CurrentUser.as_view(queryset=Client.objects.all()), name='me'),
    path('computerShop/clientById/<int:userId>', UserById.as_view(queryset=Client.objects.all()), name='clientById'),
    path('computerShop/filter-by-name/', FilterByName.as_view(), name='filter-by-name'),
    path('computerShop/filter-by-price/', FilterByPrice.as_view(), name='filter-by-price'),
    path('computerShop/filter-by-nameAndPrice/', FilterByPriceAndName.as_view(), name='filter-by-nameAndPrice'),

    # Fav
    path('computerShop/addFav/', AddFav.as_view(), name='addFav'),
    path('computerShop/fav/', Fav.as_view(queryset=Favourite.objects.all()), name='fav'),
    path('computerShop/deleteFav/<int:favId>', DeleteFav.as_view(), name='deletefav'),
    path('computerShop/favById/<int:favId>', GetFavId.as_view(), name='favById'),

    # ////////////////////

    # Order
    path('computerShop/addOrder/', AddOrder.as_view(), name='addOrder'),
    path('computerShop/order/', Orders.as_view(queryset=Order.objects.all()), name='order'),
    path('computerShop/editOrder/<int:orderId>', EditOrder.as_view(), name='editOrder'),
    path('computerShop/deleteOrder/<int:orderId>', DeleteOrder.as_view(), name='deleteOrder'),
    path('computerShop/orderById/<int:orderId>', GetOrderId.as_view(), name='orderById'),
    # //////////////////////

    # //// ADMIN /////

    # section
    path('computerShop/addSections/', AddSections.as_view(), name='addSections'),
    path('computerShop/editSection/<int:sectionId>', EditSection.as_view(), name='editSection'),
    path('computerShop/deleteSection/<int:sectionId>', DeleteSection.as_view(), name='deleteSection'),
    path('computerShop/sections/', Sections.as_view(queryset=Section.objects.all()), name='sections'),
    path('computerShop/sectionById/<int:sectionId>', GetSectionId.as_view(), name='sectionById'),
    # ////////////////

    # prooducts
    path('computerShop/addProducts/', AddProducts.as_view(), name='addProducts'),
    path('computerShop/editProduct/<int:productId>', EditProduct.as_view(), name='editProduct'),
    path('computerShop/deleteProduct/<int:productId>', DeleteProduct.as_view(), name='deleteProduct'),
    path('computerShop/products/', Products.as_view(queryset=Product.objects.all()), name='products'),
    path('computerShop/oldProducts/', OldProducts.as_view(), name='oldProducts'),
    path('computerShop/newProducts/', NewProducts.as_view(), name='newProducts'),
    path('computerShop/productById/<int:productId>', GetProductId.as_view(), name='productById'),
    # ////////////////

    # offer
    path('computerShop/addOffers/', AddOffers.as_view(), name='addOffer'),
    path('computerShop/editOffer/<int:offerId>', EditOffer.as_view(), name='editOffer'),
    path('computerShop/deleteOffer/<int:offerId>', DeleteOffer.as_view(), name='deleteOffer'),
    path('computerShop/offers/', Offers.as_view(queryset=Offer.objects.all()), name='offer'),
    path('computerShop/offerById/<int:offerId>', GetOfferId.as_view(), name='offerById'),
]
