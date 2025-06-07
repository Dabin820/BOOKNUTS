<!-- views/ThreadListView.vue -->
<template>
  <div class="thread-page-wrapper">
    <section class="container bg-white py-5">
      <h3 class="fw-bold mb-4">ThreadList</h3>
      <!-- 검색창 -->
      <div class="mb-4">
        <input
          class="form-control search-bar"
          placeholder="Search..."
          type="text"
          v-model="threadStore.searchQuery"
        >
      </div>
  
      <!-- 카테고리 토글 -->
      <div class="mb-4 d-flex flex-wrap gap-2">
        <button
          class="category-btn"
          :class="threadStore.selectedCategory === 'all' ? 'btn-warning text-white' : 'btn btn-light'"
          @click="threadStore.selectedCategory = 'all'; threadStore.getThreads();"
        >전체</button>
  
        <button
          v-for="cat in categoryStore.categories"
          :key="cat.id"
          class="category-btn"
          :class="threadStore.selectedCategory === cat.id ? 'btn-warning text-white' : 'btn btn-light'"
          @click="threadStore.selectedCategory = cat.id; threadStore.getThreads();"
        >
          {{ cat.name }}
        </button>
      </div>
    </section>

    <section class="thread-section-background px-4 py-5">
      <div class="container">

        <div class="row g-4">
          <div 
            class="col-md-4" 
            v-for="thread in threadStore.filteredThreads" 
            :key="thread.id"
          >
          <!-- RouterLink 로 감싸기 -->
          <RouterLink
            :to="{ 
              name: 'ThreadDetailView', 
              params: { threadId: thread.id } 
            }"
          >
          <ThreadItem :thread="thread" />
        </RouterLink>
          </div>
        </div>
    
        <!-- 페이지네이션 -->
        <div class="mt-4 d-flex justify-content-center align-items-center gap-3">
          <button
            class="btn btn-outline-secondary"
            :disabled="threadStore.currentPage === 1"
            @click="threadStore.currentPage--"
          >이전</button>
    
          <span>{{ threadStore.currentPage }} / {{ threadStore.totalPages }}</span>
    
          <button
            class="btn btn-outline-secondary"
            :disabled="threadStore.currentPage === threadStore.totalPages"
            @click="threadStore.currentPage++"
          >다음</button>
        </div>
      </div>
    </section>
  </div>
</template>



<script setup>
  import { onMounted, watch } from 'vue'
  import ThreadItem from '@/components/ThreadItem.vue'
  import { useThreadStore } from '@/stores/threads'
  import { useCategoryStore } from '@/stores/categories'
  import {RouterLink} from 'vue-router'
  const threadStore = useThreadStore()
  const categoryStore = useCategoryStore()

  // 초기 실행
  onMounted(() => {
    threadStore.searchQuery = ''
    threadStore.getThreads()
  })

  // 검색어가 바뀔 때마다 currentPage 초기화화
  watch(
    () => threadStore.searchQuery,
    () => {
      threadStore.currentPage = 1
    }
  )

</script>

<style scoped>

</style>