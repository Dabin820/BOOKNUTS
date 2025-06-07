# books/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Thread, Comment,Category,UserLibrary
from .serializers import BookSerializer, ThreadSerializer, CommentSerializer,CategorySerializer, UserLibrarySerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer, UserUpdateSerializer
from django.db.models import Count
from books.utils import generate_image_with_openai


#Category
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all().order_by('id')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# Book
@api_view(['GET'])
def book_list(request):
    category_id = request.GET.get('category')
    if category_id:
        books = get_list_or_404(Book.objects.filter(category__id=category_id).order_by('-pub_date'))
    else:
        books = get_list_or_404(Book.objects.order_by('-pub_date'))
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def book_detail(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['GET'])  # 책 상세 페이지에서 스레드 미리보기
def book_threads_preview(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    threads = Thread.objects.filter(book=book) \
        .annotate(like_count=Count('likes')) \
        .order_by('-like_count', '-created_at')[:2]
    serializer = ThreadSerializer(threads, many=True,context={'request': request})
    return Response(serializer.data)


# Thread - 수정: 쿼리셋이 비면 빈 배열을 반환하도록 (RESTful)
@api_view(['GET'])
def thread_list(request):
    category_id = request.GET.get('category')
    user_pk = request.GET.get('user_pk')
    if category_id:
        threads = Thread.objects.filter(book__category_id=category_id).order_by('-created_at')
    else:
        threads = Thread.objects.order_by('-created_at')
    # 특정 유저가 작성한 thread 필터링할 수 있도록
    if user_pk:
        threads = threads.filter(user__pk=user_pk)  # ← 추가
    serializer = ThreadSerializer(threads, many=True,context={'request': request})
    return Response(serializer.data)



@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def thread_create(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'GET':
        threads = Thread.objects.filter(book=book).order_by('-created_at')
        serializer = ThreadSerializer(threads, many=True,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            thread = serializer.save(user=request.user, book=book)
            
            # ✅ OpenAI 이미지 생성
            generated_img_path = generate_image_with_openai(
                thread,
                thread.title,
                thread.content,
                book.title,
                book.author
            )
            print('[DEBUG] 생성된 이미지 경로:', generated_img_path)

            if generated_img_path:
                thread.cover_img.name = generated_img_path  # MEDIA_ROOT 이하 경로만 지정
                thread.save()

            return Response(ThreadSerializer(thread,context={'request': request}).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@permission_classes([IsAuthenticated])
@api_view(['GET','PUT','DELETE'])
def thread_detail(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    # 삭제 및 수정 권한 체크
    if request.method in ['PUT', 'DELETE']:
        if thread.user != request.user:
            return Response(
                {"detail": "본인만 수정/삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

    if request.method == 'GET':
        serializer = ThreadSerializer(thread, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ThreadSerializer(thread, data=request.data, partial=True,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        thread.delete()
        return Response({"detail": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def thread_like(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    user = request.user
    if user in thread.likes.all():
        thread.likes.remove(user)
        liked = False
    else:
        thread.likes.add(user)
        liked = True
    return Response({'liked':liked, 'like_count':thread.likes.count()})


# Comment
@api_view(['GET','POST'])
def comment_list(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    if request.method == 'GET':
        comments = thread.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return Response({'detail':'권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Profile
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_detail(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    # GET: 누구나(로그인 유저라면) 볼 수 있게
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    # PUT/PATCH: 본인만 수정 가능
    if request.method in ['PUT', 'PATCH']:
        if request.user != user:
            return Response({'detail':'권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE: 본인만 삭제 가능
    if request.method == 'DELETE':
        if request.user != user:
            return Response({'detail':'권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def library_add(request):
    user = request.user
    # isbn = request.data.get('book_id')
    # book = get_object_or_404(Book, pk=isbn)
    serializer = UserLibrarySerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.validated_data['book']
        # 중복 체크
        if UserLibrary.objects.filter(user=user, book=book).exists():
            return Response({'detail': '이미 내 서재에 담긴 책입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        # serializer.save(user=user, book=book)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('📌 serializer errors:', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def library_list(request):
    # 쿼리 파라미터로 user_pk를 받을 수 있게
    user_pk = request.GET.get('user_pk')
    if user_pk:
        user = get_object_or_404(get_user_model(), pk=user_pk)
    else:
        user = request.user
    # 최신순으로 정렬하고, 최대 6개만 반환
    user_library = UserLibrary.objects.filter(user=user).order_by('-saved_date')[:6]
    serializer = UserLibrarySerializer(user_library, many=True)
    return Response(serializer.data)
