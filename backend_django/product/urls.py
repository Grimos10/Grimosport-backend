from django.urls import path, include

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductList.as_view()),
    path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('more-buyed-products/', views.MoreBuyedProductList.as_view()),
    path('add-product/', views.SetProduct.as_view()),
    path('get-categories/', views.GetCategories.as_view()),
    path('stats/', views.ProductStats.as_view()),
]