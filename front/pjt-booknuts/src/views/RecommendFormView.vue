<!-- views/RecommendFormView.vue -->
<template>
  <div class="container d-flex flex-column align-items-center justify-content-center" style="min-height: 80vh;">
    <h2 class="fw-bold text-center mb-4">토리에게 물어보세요</h2>
    <form @submit.prevent="onSubmit" class="w-100" style="max-width: 700px;">
      <div class="input-group shadow rounded-pill overflow-hidden">
        <!-- 캐릭터 이미지 -->
        <span class="input-group-text bg-white border-0">
          <img src="@/assets/image/maintori.png" alt="tori" width="30" height="30" />
        </span>
        <!-- 입력창 -->
        <input v-model="query" class="form-control border-0" type="text" placeholder="읽고 싶은 책의 분위기, 상황 등을 자유롭게 입력해보세요!" />
        <button type="submit" :disabled="loading" class="btn btn-warning rounded-0 px-4">
          <i class="bi bi-arrow-right"></i>
        </button>
      </div>
    </form>
    <!-- 로딩/에러 메세지 -->
    <div v-if="loading" class="text-muted mt-3">
      <img
        src="@/assets/image/findingtori.png"
        alt="로딩 중 캐릭터"
        class="mb-3"
        style="width: 150px;"
      />
      <p class="fw-semibold">추천 중입니다..<br>잠시만 기다려주세요..</p>
    </div>
    <div v-if="error" class="text-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRecommendStore } from '@/stores/recommends'

const recommendStore = useRecommendStore()

const query = ref('')
const router = useRouter()
const loading = computed(() => recommendStore.loading)
const error = computed(() => recommendStore.error)

async function onSubmit() {
  if (!query.value.trim()) return
  await recommendStore.fetchRecommendations(query.value)
  if (!recommendStore.error) {
    router.push({ name: 'RecommendView' })
  }
}
</script>

<style scoped>
/* 아이콘, 입력창 정렬을 위해 padding 조정 */
.input-group-text img {
  object-fit: cover;
  border-radius: 50%;
}
</style>

