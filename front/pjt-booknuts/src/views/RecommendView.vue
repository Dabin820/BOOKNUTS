<template>
  <div class="container my-5">
    <h3 class="fw-bold mb-4">다음과 같은 책은 어떠신가요? 📚</h3>

    <div class="vstack gap-4">
      <div v-for="book in recommendations" :key="book.isbn" class="card shadow-sm p-3">
        <router-link
            :to="{ name: 'BookDetailView', params: { bookId: book.isbn } }"
            class="d-flex text-decoration-none text-dark"
        >
        <div class="flex-shrink-0 me-3">
          <img :src="book.cover" alt="book.title" class="rounded me-3" style="width: 100px; height: auto;"/>
        </div>
        <div class="flex-grow-1">
            <h5 class="fw-bold mb-1">{{ book.title }}</h5>
            <p class="mb-1"><strong>저자:</strong> {{ book.author }}</p>
            <p class="text-muted mb-1">{{ book.description.length > 100 ? book.description.slice(0, 100) + '...' : book.description }}</p>
            <!-- <p><strong>저자 정보:</strong> {{ book.author_info }}</p> -->
            <p class="mb-0"><strong>페이지 수:</strong> {{ book.itemPage }} 쪽</p>
        </div>
      </router-link>
      </div>
    </div>

     <!-- 버튼 영역 -->
    <div class="mt-5">
      <h5 class="fw-bold mb-3">마음에 들지 않는다면? 🥺</h5>
      <div class="d-flex flex-wrap gap-3">
        <button class="btn btn-warning px-4" @click="goToRecommendForm">다시 추천 받기</button>
        <button class="btn btn-outline-secondary px-4" @click="goToMain">홈으로 돌아가기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useRecommendStore } from '@/stores/recommends'

  const router = useRouter()
  const recommendStore = useRecommendStore()
  const recommendations = computed(() => recommendStore.recommendations)

  // 추천 종료 버튼 클릭 시 메인으로 이동
  const goToMain = () => {
    recommendStore.clearRecommendations()
    router.push({ name: 'MainView' })
  }

  // 추천 다시 받기
  const goToRecommendForm = () => {
    recommendStore.clearRecommendations()
    router.push({ name: 'RecommendFormView' })
  }

</script>

<style scoped>

</style>