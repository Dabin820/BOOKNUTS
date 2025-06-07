<!-- views/ThreadCreateView.vue -->
<template>
  <div>
    <h3 class="fw-bold mt-3 mb-0 text-center">게시글 작성</h3>
    <ThreadCreateForm 
      v-if="book"
      :key="book.id"
      :book="book" 
    />
    <div v-else>도서 정보를 불러오는 중...</div>
  </div>
</template>


<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  import { useThreadStore } from '@/stores/threads'
  import ThreadCreateForm from '@/components/ThreadCreateForm.vue'

  const route = useRoute()
  const threadStore = useThreadStore()

  const book = ref(null)
  
  onMounted(async () => {
    const bookId = route.params.bookId
    try {
      const response = await axios({
        method: 'GET',
        url: `${threadStore.API_URL}/books/${bookId}/`,
      })
      book.value = response.data
    } catch (error) {
      alert('도서 정보를 불러올 수 없습니다')
      console.error('도서 정보 불러오기 실패:', error)
      book.value = null
    }
  })

</script>

<style scoped>

</style>