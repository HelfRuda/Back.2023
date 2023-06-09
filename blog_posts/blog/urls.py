from django.urls import path, include
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .api import AllPostsAPI, AddPostAPI, EditPostAPI, DeletePostAPI, AddCommentsAPI

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="API for my web blog",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


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
               path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
               path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
               path('api/all_posts/', AllPostsAPI.as_view(), name='all_posts_api'),
               path('api/add_post/', AddPostAPI.as_view(), name='add_post_api'),
               path('api/edit_post/<int:pk>/', EditPostAPI.as_view(), name='edit_post_api'),
               path('api/delete_post/<int:pk>/', DeletePostAPI.as_view(), name='delete_post_api'),
               path('api/add_comments/<int:pk>/', AddCommentsAPI.as_view(), name='add_comments_api'),]
