from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from Main import apiviews

urlpatterns = [
    # path('api/categories', apiviews.CategoryList.as_view()),
    # path('api/categories/<str:catname>', apiviews.CategoryItems.as_view()),
    # path('api/item/<int:id>', apiviews.ItemSingle.as_view()),
    # path('api/search/<str:text>', apiviews.SearchedItems.as_view()),
    # path('api/item_card/<int:id>', apiviews.ItemCard.as_view()),
    path('api/complains', apiviews.ComplainList.as_view()),
    path('api/complain/<int:id>', apiviews.ComplainDetails.as_view()),
    path('api/complain/add', apiviews.ComplainCreate),


    # path('api/user/profile/<str:token>', apiviews.CustomerProfile.as_view()),
    # path('api/user/exist', apiviews.UserExists),
    # path('api/user/login', apiviews.UserVerification),
]
urlpatterns = format_suffix_patterns(urlpatterns)
