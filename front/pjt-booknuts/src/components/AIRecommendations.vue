<template>
  <section class=" mian-container bg-brown text-white d-flex justify-content-between align-items-center px-5 py-4 m-0 w-100">
    <h3 class="mb-0 fw-bold">토리에게 책 추천 받기</h3>
    <button class="btn btn-warning fw-bold px-4 py-2" @click="goToRecommendForm">추천 받기</button>
  </section>
</template>


<script setup>
  import { useRouter } from 'vue-router'

  const router = useRouter()

  const goToRecommendForm = function () {
    router.push({ name: 'RecommendFormView' })
  }
</script>


<style scoped>
.bg-brown {
  background-color: #a45c1e;
}
</style>
