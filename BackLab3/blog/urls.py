from django.urls import path
from . import views

urlpatterns = [path('', views.LoginView.as_view(), name='login'),
               path('register/', views.RegistrationView.as_view(), name='registration'),
               path('index/', views.CategoryView.as_view(), name='home'),
               path('all_posts/', views.AllPostsView.as_view(), name='all_posts'),
               path('all_posts/<int:pk>/update/', views.EditPostView.as_view(), name='edit_post'),
               path('all_posts/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
               path('add_post/', views.AddPostView.as_view(), name='add_post'),
               path('category/<int:category_id>/', views.PostView.as_view(), name='post_list_by_category'),
               path('category/<int:category_id>/<int:pk>/', views.PostDetail.as_view(), name='blog_detail'),
               path('category/<int:category_id>/review/<int:pk>/', views.AddComments.as_view(), name='add_comments'),
               path('category/<int:category_id>/<int:pk>/delete/', views.PostDetail.as_view(), name='post_delete'),]
