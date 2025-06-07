<!-- views/LoadingSpinner.vue -->
<template>
  <div class="position-fixed top-0 start-0 w-100 h-100 d-flex flex-column justify-content-center align-items-center bg-white bg-opacity-75" style="z-index: 1050;">
    <!-- 토리 그림 이미지로 로딩 표시 -->
    <img
      src="@/assets/image/paintingtori.png"
      alt="로딩 중"
      style="width: 150px; height: auto;"
      class="mb-3"
    />
    <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
      <span class="visually-hidden">Loading...</span>
    </div>
    <p class="mt-3 fs-5 text-dark">이미지를 생성 중입니다...</p>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>