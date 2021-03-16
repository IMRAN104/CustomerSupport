from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ecom import apiviews, ecom_cat_views, views

urlpatterns = [
    path('api/user/profile/<str:token>', apiviews.CustomerProfile.as_view()),

    path('api/user/exist', apiviews.UserExists),
    path('api/user/login', apiviews.UserVerification),
    path('api/mobile_verification', apiviews.MobileVerification),
    path('api/email_verification', apiviews.EmailVerification),
    path('api/email_validation', apiviews.EmailValidation),
    
    path('api/mobile_OTP_send', apiviews.MobileOTPSend),
    path('api/mobile_OTP_resend', apiviews.MobileOTPResend),
    path('api/email_OTP_send', apiviews.EmailOTPSend),
    path('api/email_OTP_resend', apiviews.EmailOTPResend),

    path('api/register', apiviews.Register),
    path('api/reset_password', apiviews.ResetPassword),

    path('items',views.ItemManagement,name='ECom-ItemManagement'),
    path('items/create', views.ItemCreate, name='ECom-ItemCreate'),
    path('items/edit/<int:id>', views.ItemEdit, name='ECom-ItemEdit'),
    path('items/view/<int:id>', views.ItemView, name='ECom-ItemView'),
    path('items/delete/<int:id>', views.ItemDelete, name='ECom-ItemDelete'),
    
    path('home_items',views.HomeItemManagement,name='ECom-HomeItemManagement'),
    path('home_items/create', views.HomeItemCreate, name='ECom-HomeItemCreate'),
    path('home_items/edit/<int:id>', views.HomeItemEdit, name='ECom-HomeItemEdit'),
    path('home_items/view/<int:id>', views.ItemView, name='ECom-HomeItemView'),

    path('home_groups',views.ItemManagement,name='ECom-HomeGroupManagement'),
    path('home_groups/create', views.HomeGroupCreate, name='ECom-HomeGroupCreate'),
    path('home_groups/edit/<int:id>', views.ItemEdit, name='ECom-HomeGroupEdit'),
    path('home_groups/view/<int:id>', views.ItemView, name='ECom-HomeGroupView'),

    path('api/categories', apiviews.CategoryList.as_view()),
    ## the next one is incomplete
    path('api/categories/<str:catname>', apiviews.CategoryItems.as_view()),
    path('api/item/<int:id>', apiviews.ItemSingle.as_view()),
    path('api/search/<str:text>', apiviews.SearchedItems.as_view()),
    path('api/item_card/<int:id>', apiviews.ItemCard.as_view()),
    path('api/home_groups', apiviews.HomeGroups.as_view()),
    path('api/offers', apiviews.OfferList.as_view()),
#     path('item/view/<int:id>/', views.eComItemView),
#     path('item/create/', views.eComItemCreate),

    path('category',ecom_cat_views.CategoryManagement,name='EComCategoryManagement'),
    path('category/create',ecom_cat_views.CategoryCreate,name='EComCategoryCreate'),
    path('category/edit/<int:id>',ecom_cat_views.CategoryEdit,name='EComCategoryEdit'),
    path('category/view/<int:id>',ecom_cat_views.CategoryView,name='EComCategoryView'),
    path('category/delete/<int:id>',ecom_cat_views.CategoryDelete,name='EComCategoryDelete'),

    # ajax load
    path('item/ajax/load-cat/', ecom_cat_views.load_cat, name="ItCrLoCat")
    
]
urlpatterns = format_suffix_patterns(urlpatterns)
