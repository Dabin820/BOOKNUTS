<!-- views/BookDetailView.vue -->
<template>
  <header>
    <!-- 버튼: 내 서재에 담기 -->
  </header>
  <div>
    <BookDetail />
  </div>

</template>


<script setup>
  import BookDetail from '@/components/BookDetail.vue'

  const props = defineProps({
    bookId: String
  })

</script>

<style scoped>

</style>