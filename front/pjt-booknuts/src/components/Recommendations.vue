<!-- views/Recommendations.vue -->
<!-- 작가 기반 -->
<template>
  <div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="loading" class="text-center my-4">
      <div class="spinner-border text-secondary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div
      v-else-if="itemBasedRecommendations && itemBasedRecommendations.length"
      class="recommend-section text-center" 
    >
      <div id="recommendCarousel" class="carousel slide mx-auto" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div
            v-for="(slide, idx) in slides"
            :key="idx"
            :class="['carousel-item', { active: idx === 0 }]"
          >
            <div class="row justify-content-center">
              <div
                v-for="book in slide"
                :key="book.isbn"
                class="col-12 col-md-6 d-flex justify-content-center"
              >
                <div class="recommend-card d-flex flex-column align-items-center">
                  <RouterLink
                    :to="{ name: 'BookDetailView', params: { bookId: book.isbn } }"
                    class="text-decoration-none text-dark mb-2"
                  >
                    <img
                        :src="book.cover"
                        alt="cover"
                        class="recommend-cover"
                      />
                  </RouterLink>
                  
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Carousel Controls -->
        <button
          class="carousel-control-prev"
          type="button"
          data-bs-target="#recommendCarousel"
          data-bs-slide="prev"
          style="left: -70px"
        >
          <span class="carousel-control-prev-icon bg-dark rounded-circle" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-control-next"
          type="button"
          data-bs-target="#recommendCarousel"
          data-bs-slide="next"
          style="right: -70px"
        >
          <span class="carousel-control-next-icon bg-dark rounded-circle" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </div>

    <div v-else class="text-muted">추천 도서를 준비 중입니다.</div>
  </div>
</template>

<script setup>
  import { computed, onMounted, watch } from 'vue'
  import { useRoute, RouterLink } from 'vue-router'
  import { storeToRefs } from 'pinia'
  import { useRecommendStore } from '@/stores/recommends'

  const route = useRoute()
  const recommendStore = useRecommendStore()
  const { itemBasedRecommendations, loading, error } = storeToRefs(recommendStore)

  const fetchData = async (bookId) => {
    await recommendStore.fetchItemBasedRecommendations(bookId)
  }

  // 한 슬라이드에 2권씩 (모바일은 1권씩, 슬라이드는 유지)
  const slides = computed(() => {
  // 반응형: 모바일(≤576px)은 1권, 그 외는 2권
  let itemsPerSlide = 2
  if (typeof window !== 'undefined' && window.innerWidth <= 576) {
    itemsPerSlide = 1
  }
  const result = []
  for (let i = 0; i < itemBasedRecommendations.value.length; i += itemsPerSlide) {
    result.push(itemBasedRecommendations.value.slice(i, i + itemsPerSlide))
  }
  return result
})

  onMounted(() => {
    fetchData(route.params.bookId)
  })

  watch(() => route.params.bookId, (newId) => {
    fetchData(newId)
    window.scrollTo({ top: 0, behavior: 'smooth' })  // 추가!
  })
</script>


<style scoped>
  .recommend-section {
    height: 400px;
    background-color: transparent; /* ✅ 배경 투명 */
  }

  .recommend-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    text-align: left;
  }

  .recommend-card {
    width: 160px;
  }

  .recommend-cover {
    width: 100%;
    max-width: 140px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 0.5rem;
  }

  .book-card-title {
    color: black;
    font-size: 1rem;
    font-weight: 500;
    max-width: 140px;
    word-wrap: break-word;
    line-height: 1.2;
    text-align: center;
  }
</style>
