from rest_framework import serializers
from django.db import models
from .models import *
import re
from django.conf import settings

def category_lineage_string(ecomcat):
        if ecomcat.level == "root":
            return ecomcat.category_name
        else:
            return category_lineage_string(ecomcat.parent)+\
                "/"+ecomcat.category_name


def get_all_children_cat(catid, catlist, depth, first=True, initcat=None):
    if depth > 8:
        return
    catlist.append(catid)
    if first:
        all_cats = eComCategory.objects.all()
    else:
        all_cats = initcat
    allchildren = []
    for cat in all_cats:
        if cat.parent_id == catid:
            allchildren.append(cat)
    for childcat in allchildren:
        get_all_children_cat(childcat.id, catlist, depth+1, False, all_cats)
    return


# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = eComItemImage
#         fields = ['image']

class ItemCardSerializer(serializers.ModelSerializer):
    #name = serializers.ReadOnlyField(source='display_name')
    #quantity = serializers.ReadOnlyField(source='coreitem.quantity')
    item_id = serializers.ReadOnlyField(source='id')

    brand = serializers.ReadOnlyField(source='ecomitemmeta.brand.name')
    quantity = serializers.SerializerMethodField('get_quantity')
    base_price = serializers.SerializerMethodField('get_base_price_float')
    offer_price = serializers.SerializerMethodField('get_offer_price_float')
    #base_price = int(serializers.ReadOnlyField(source='base_price'))
    #offer_price = int(serializers.ReadOnlyField(source='offer_price'))
    thumbnail = serializers.SerializerMethodField('get_thumbnail')
    
    
    class Meta:
        model = eComItem
        fields = ['item_id', 'display_name', 
        'base_price', 'offer_price', 'thumbnail', 
        'brand', 'quantity']

    def get_base_price_float(self, ecomitem):
        return float(ecomitem.base_price)
    
    def get_offer_price_float(self, ecomitem):
        try:
            return float(ecomitem.offer_price)
        except:
            return 0.0
    
    def get_quantity(self, ecomitem):
        try:
            return ecomitem.item.quantity - ecomitem.ecomitemmeta.safety_stock
        except:
            return ecomitem.item.quantity

    def get_thumbnail(self, ecomitem):
        try:
            #print(ecomitem.thumbnail.url)
            return ecomitem.thumbnail.url
        except:
            return None

class ItemSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='id')
    images = serializers.SerializerMethodField('images_from_image_set')
    #images = ProductImageSerializer(source='ecomitemimage_set', read_only=True, many=True)
    category = serializers.SerializerMethodField('get_category_lineage')
    
    brand = serializers.ReadOnlyField(source='ecomitemmeta.brand.name')
    short_description = serializers.ReadOnlyField(source='ecomitemmeta.short_description')
    long_description = serializers.ReadOnlyField(source='ecomitemmeta.long_description')
    rating = serializers.ReadOnlyField(source='ecomitemmeta.rating')
    safety_stock = serializers.ReadOnlyField(source='ecomitemmeta.safety_stock')
    re_order_stock = serializers.ReadOnlyField(source='ecomitemmeta.re_order_stock')
    max_sale_stock = serializers.ReadOnlyField(source='ecomitemmeta.max_sale_stock')
    
    thumbnail = serializers.SerializerMethodField('get_thumbnail')
    related_products = serializers.SerializerMethodField('get_related_products')
    #similar_products = serializers.ReadOnlyField(source='ecomitemmeta.similar_products')
    similar_products = serializers.SerializerMethodField('get_similar_products')

    quantity = serializers.ReadOnlyField(source='item.quantity')
    base_price = serializers.SerializerMethodField('get_base_price_float')
    offer_price = serializers.SerializerMethodField('get_offer_price_float')
    class Meta:
        model = eComItem
        fields = ['item_id', 
        'display_name', 
        'category',
        'thumbnail',
        'base_price',
        'offer_price',

        'brand',
        'short_description',
        'long_description',
        'rating',
        'safety_stock',
        're_order_stock',
        'max_sale_stock',
        'related_products',
        'similar_products',

        'images',
        'quantity'
        ]
    
    def get_thumbnail(self, ecomitem):
        try:
            #print(ecomitem.thumbnail.url)
            return ecomitem.thumbnail.url
        except:
            return None
    
    def images_from_image_set(self, ecomitem):
        try:
            return [img.image.url for img in ecomitem.ecomitemimage_set.get_queryset()]
        except:
            return []
                
    def get_base_price_float(self, ecomitem):
        return float(ecomitem.base_price)
    
    def get_offer_price_float(self, ecomitem):
        try:
            return float(ecomitem.offer_price)
        except:
            return 0.0
    
    def get_category_lineage(self, ecomitem):
        try:
            return category_lineage_string(ecomitem.category)
        except:
            return None
    
    def get_similar_products(self, ecomitem):
        try:
            similars = re.split('/', ecomitem.ecomitemmeta.similar_products)
            similars = [int(sim) for sim in similars]
            items = eComItem.objects.filter(id__in=similars)
        except:
            return []
        
        sez = ItemCardSerializer(data=items, many=True)
        sez.is_valid()
        return sez.data

    def get_related_products(self, ecomitem):
        try:
            relateds = re.split('/', ecomitem.ecomitemmeta.related_products)
            relateds = [int(sim) for sim in relateds]
            items = eComItem.objects.filter(id__in=relateds)
        except:
            return []
        
        sez = ItemCardSerializer(data=items, many=True)
        sez.is_valid()
        return sez.data
    

    
class CategoryHierarchySerializer(serializers.ModelSerializer):
    #parent_name = serializers.SerializerMethodField('get_parentname')
    parent_name = serializers.ReadOnlyField(source='category_lineage_string')
    class Meta:
        model = eComCategory
        fields = ['id', 'category_name', 'parent', 'level', 'parent_name', 'root']
    
        
class CategoryItemsSerializer(serializers.ModelSerializer):
    """
    Returns only those items who has 'this' category as it's category.
    i.e. only works for leaf categories.
    Need to update it.
    """
    items = serializers.SerializerMethodField('category_items_union')
    #items = ItemCardSerializer(read_only=True, many=True, source='ecomitem_set')
    class Meta:
        model = eComCategory
        fields = ['category_name', 'id', 'items']

    def category_items_union(self, cat):
        cat_id_list = []
        get_all_children_cat(cat.id, cat_id_list, 0)
        items = eComItem.objects.filter(category__in=cat_id_list)
        sez = ItemCardSerializer(data=items, many=True)
        sez.is_valid()
        return sez.data
        
        
class OfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        fields = '__all__'

class HomeItemSerializer(serializers.ModelSerializer):
    item = ItemCardSerializer(read_only=True)
    class Meta:
        model = HomeItem
        fields = ['item']

class HomeGroupSerializer(serializers.ModelSerializer):
    #items = HomeItemSerializer(read_only=True, many=True, source='homeitem_set')
    items = serializers.SerializerMethodField('get_active_home_items')
    class Meta:
        model = HomeGroup
        fields = ['group_order', 'group_name', 'items']
    
    def get_active_home_items(self, homegroup):
        homeitems = homegroup.homeitem_set.get_queryset().filter(is_archived=False)
        sez = HomeItemSerializer(data=homeitems, many=True)
        sez.is_valid()
        return sez.data


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'mobile', 'email', 'address', 'city', 'district', 'postcode',\
        'country', 'gender']
