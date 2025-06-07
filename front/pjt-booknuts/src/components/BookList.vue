<!-- views/BookList.vue -->
<template>
  <div class="book-page-wrapper">
    <section class="container bg-white py-5">
      <h3 class="fw-bold mb-4">BookList</h3>
      <!-- 검색창 -->
       <div class="mb-4">
         <input
           v-model="searchQuery"
           class="form-control search-bar"
           placeholder="검색어를 입력하세요"
           type="text"
         />
       </div>

       
           <!-- 카테고리 버튼 -->
           <div class="mb-4 d-flex flex-wrap gap-2">
             <button
               class="category-btn"
               :class="selectedCategory === null ? 'btn-warning text-white' : 'btn btn-light'"
               @click="clearCategory"
             >전체</button>
       
             <button
               v-for="category in categories"
               :key="category.id"
               class="category-btn"
               :class="selectedCategory === category.id ? 'btn-warning text-white' : 'btn btn-light'"
               @click="selectCategory(category.id)"
             >
               {{ category.name }}
             </button>
         </div>
    </section>

    <section class="book-section-background px-4 py-5">
      <div class="container">
        <!-- 📖 책 목록 -->
        <div class="row g-4">
          <div class="col-md-4" v-for="book in paginatedBooks" :key="book.isbn">
            <BookCard :book="book" />
          </div>
        </div>
        <!-- 📄 페이지네이션 -->
        <div class="mt-4 d-flex justify-content-center align-items-center gap-3">
          <button
            class="btn btn-outline-secondary"
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            이전
          </button>
      
          <span>{{ currentPage }} / {{ totalPages }}</span>
      
          <button
            class="btn btn-outline-secondary"
            :disabled="currentPage === totalPages"
            @click="currentPage++"
          >
            다음
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
  import { onMounted, watch } from 'vue'
  import { useBookStore } from '@/stores/books'
  import { useCategoryStore } from '@/stores/categories'
  import { storeToRefs } from 'pinia'
  import BookCard from '@/components/BookCard.vue'

  // 스토어 설정
  const bookStore = useBookStore()
  const categoryStore = useCategoryStore()

  // storeToRefs 추출
  const {
    paginatedBooks,
    searchQuery,
    currentPage,
    totalPages,
    selectedCategory
  } = storeToRefs(bookStore)

  const { categories } = storeToRefs(categoryStore)

  // 카테고리 선택/해제
  const selectCategory = (categoryId) => {
    bookStore.selectedCategory = categoryId
    bookStore.getBooks()
  }

  const clearCategory = () => {
    bookStore.selectedCategory = null
    bookStore.getBooks()
  }

  // 초기 실행
  onMounted(() => {
    bookStore.searchQuery = ''
    categoryStore.getCategories()
    bookStore.getBooks()
  })

  // 검색어가 바뀔 때마다 currentPage 초기화
  watch(
    () => bookStore.searchQuery,
    () => {
      bookStore.currentPage = 1
    }
  )

</script>
