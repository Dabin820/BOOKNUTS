<!-- views/BookCard.vue -->
<template>
  <RouterLink
    v-if="book"
    :to="{ name: 'BookDetailView', params: { bookId: book.isbn } }"
    class="text-decoration-none text-dark"
  >
    <div class="thread-card p-3 rounded shadow-sm h-100">
      <img :src="book.cover" alt="cover" class="img-fluid rounded mb-3" />
      <p class="thread-title fw-bold text-truncate">{{ book.title }}</p>
      <p class="text-muted small author-text text-truncate">{{ book.author }}</p>
    </div>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'
const props = defineProps({
  book: Object,
})
</script>

<style scoped>
.author-text {
  font-size: 0.85rem;
}
</style>
