from django.conf import settings
import openai
from books.models import Book
from books.serializers import BookSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
import re
from collections import defaultdict
import json
from pathlib import Path 
from difflib import SequenceMatcher


class RecommendBookAPIView(APIView):
    def post(self, request):
        user_query = request.data.get('query', '').strip()
        if not user_query:
            return Response({"error": "query is required"}, status=400)

        try:
            # GPT로 키워드 최대 6개 추출
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            keyword_prompt = f"""
            다음 사용자 입력 문장에서 의미 있는 핵심 키워드를 최대 6개 추출하세요.
            사용자의 쿼리가 짧더라도 최대한 맥락을 고려하여 세분화된 키워드를 추출하세요.
            너무 일반적인 단어(도서,책,읽기)는 피하고, 불용어(는,은,이,가,요,을 등)도 빼고 쉼표로 구분하세요.
            [입력]
            {user_query}
            예시 출력: 사랑, 우정, 트라우마, 성장, 가족, 치유
            """
            chat = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 도서 추천용 키워드 추출에 능한 언어 전문가입니다."},
                    {"role": "user", "content": keyword_prompt},
                ],
                max_tokens=200,
                temperature=0.2,
            )
            extracted_keywords = re.split(r'[,\s]+', chat.choices[0].message.content.strip())
            extracted_keywords = [k.strip() for k in extracted_keywords if k.strip()]
            print(f"[DEBUG] GPT 키워드: {extracted_keywords}")

            # isbn_keywords.json 로드
            isbn_keywords_path = Path(__file__).resolve().parent / 'isbn_keywords.json'
            with open(isbn_keywords_path, encoding='utf-8') as f:
                isbn_keyword_data = json.load(f)

             # ✅ 유사도 함수 (title 비교 포함)
            def keyword_similarity(gpt_keywords, book_keywords, book_title):
                score = 0
                # 1. 키워드와 isbn 키워드 비교
                for gk in gpt_keywords:
                    for bk in book_keywords:
                        if SequenceMatcher(None, gk, bk).ratio() > 0.8:
                            score += 1
                # 2. 키워드와 title 비교
                for gk in gpt_keywords:
                    if gk in book_title:
                        score += 1  # 단순 포함일 경우 +1 점수 (추가 가중치 가능)
                return score

            # ✅ isbn별 점수 계산 (keywords + title 기준)
            isbn_scores = []
            for entry in isbn_keyword_data:
                score = keyword_similarity(
                    extracted_keywords,
                    entry.get('keywords', []),
                    entry.get('title', '')
                )
                if score > 0:
                    isbn_scores.append((entry['isbn'], score))
                    
            if not isbn_scores:
                return Response({"error": "유사한 도서를 찾을 수 없습니다."}, status=204)

            # 상위 3개 isbn 선택
            top_isbns = [isbn for isbn, _ in sorted(isbn_scores, key=lambda x: x[1], reverse=True)[:5]]

            # DB에서 도서 조회 및 정렬
            books_qs = Book.objects.filter(isbn__in=top_isbns)
            books_dict = {b.isbn: b for b in books_qs}
            sorted_books = [books_dict[isbn] for isbn in top_isbns if isbn in books_dict]

            serializer = BookSerializer(sorted_books, many=True)
            return Response(serializer.data)

        except Exception as e:
            print(f"[RecommendBookAPIView][ERROR] {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 아이템 기반 추천 API
class BookItemBasedRecommendAPIView(APIView):
    def get(self, request, book_pk):
        try:
            base_book = Book.objects.get(pk=book_pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # 1. 같은 author (자기 자신 제외)
        books_author = Book.objects.filter(
            author=base_book.author
        ).exclude(pk=base_book.pk)

        # 2. 같은 publisher (자기 자신, 이미 추천된 것 제외)
        books_publisher = Book.objects.filter(
            publisher=base_book.publisher
        ).exclude(pk=base_book.pk).exclude(pk__in=books_author.values_list('pk', flat=True))

        # 3. 같은 category (자기 자신, 이미 추천된 것 제외)
        books_category = Book.objects.filter(
            category=base_book.category
        ).exclude(pk=base_book.pk).exclude(pk__in=books_author.values_list('pk', flat=True)).exclude(pk__in=books_publisher.values_list('pk', flat=True))

        # 최대 6개까지 우선순위대로 합치기
        recommendations = list(books_author[:6])
        if len(recommendations) < 6:
            recommendations += list(books_publisher[:(6 - len(recommendations))])
        if len(recommendations) < 6:
            recommendations += list(books_category[:(6 - len(recommendations))])

        serializer = BookSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)