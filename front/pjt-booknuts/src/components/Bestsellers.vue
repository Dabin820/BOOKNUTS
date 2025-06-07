<!-- views/Bestsellers.vue -->
<template>
  <section class="container py-5">
    <h3 class="fw-bold mb-4">베스트셀러 ⭐️</h3>

    <div id="bestsellerCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">

        <!-- N슬라이드 자동 생성 -->
        <div
          v-for="(slideBooks, idx) in chunkedBestsellers"
          :key="idx"
          :class="['carousel-item', { active: idx === 0 }]"
        >
          <div class="d-flex justify-content-evenly flex-wrap gap-4">
            <div
              v-for="book in slideBooks"
              :key="book.isbn"
              class="bestseller-card p-3 rounded shadow-sm text-center"
            >
              <RouterLink
                :to="{ name: 'BookDetailView', params: { bookId: book.isbn } }"
                class="text-decoration-none text-dark"
              >
                <img
                  :src="book.cover"
                  alt="cover"
                  class="img-fluid mb-3"
                  style="height: 250px; object-fit: cover; border-radius: 6px;"
                />
                <h5 class="book-card-title">{{ book.title }}</h5>
                <p class="book-card-author text-muted">{{ book.author }}</p>
              </RouterLink>
            </div>
          </div>
        </div>

      </div>

      <!-- 컨트롤 버튼 -->
      <button class="carousel-control-prev" type="button" data-bs-target="#bestsellerCarousel" data-bs-slide="prev" style="left: -40px">
        <span class="carousel-control-prev-icon bg-dark rounded-circle" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#bestsellerCarousel" data-bs-slide="next" style="right: -40px">
        <span class="carousel-control-next-icon bg-dark rounded-circle" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </section>
</template>

<script setup>
  import { onMounted, computed } from 'vue'
  import { useBookStore } from '@/stores/books'
  import { storeToRefs } from 'pinia'

  const store = useBookStore()
  const { bestsellers } = storeToRefs(store)

  // 4권씩 나누는 유틸
  const chunkedBestsellers = computed(() => {
    const chunkSize = 4
    const arr = []
    for (let i = 0; i < bestsellers.value.length; i += chunkSize) {
      arr.push(bestsellers.value.slice(i, i + chunkSize))
    }
    return arr
  })

  // onMounted(() => {
  //   store.getBooks()
  // })
</script>

<style scoped>
  .bestseller-card {
    width: 180px;
    background-color: #fff;
    transition: transform 0.2s ease;
  }
  .bestseller-card:hover {
    transform: translateY(-5px);
  }

  .book-card-title {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .book-card-author {
    font-size: 0.875rem;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>
