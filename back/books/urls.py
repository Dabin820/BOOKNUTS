# books/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
### 추천
from .recommendation import RecommendBookAPIView, BookItemBasedRecommendAPIView


urlpatterns = [
    # Recommendation 
    path('books/recommend/', RecommendBookAPIView.as_view(), name='book-recommend'),
    path('books/<str:book_pk>/item-recommend/', BookItemBasedRecommendAPIView.as_view(), name='book-item-recommend'),
    
    # Book
    path('books/', views.book_list),
    path('books/<str:book_pk>/', views.book_detail),
    path('profile/library/add/', views.library_add),   # 유저 라이브러리에 추가
    path('books/<str:book_pk>/threads-preview/', views.book_threads_preview),   # 책 상세 페이지에서 스레드 미리보기

    # Thread
    path('threads/', views.thread_list),    # thread 전체 (책 상관없이)
    path('books/<str:book_pk>/threads/', views.thread_create),
    path('threads/<int:thread_pk>/', views.thread_detail),
    path('threads/<int:thread_pk>/like/', views.thread_like),

    # Comment
    path('threads/<int:thread_pk>/comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_delete),

    # Profile
    path('profile/<int:user_pk>/', views.profile_detail),
    path('profile/library/', views.library_list),
    
    #Category
    path('categories/',views.category_list),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
