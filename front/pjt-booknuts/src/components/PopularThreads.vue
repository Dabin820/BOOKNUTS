<!-- views/PopularThreads.vue -->
<template>
  <div class="container py-5">
    <h3 class="fw-bold mb-4">인기 쓰레드 🔥</h3>
    <div class="row g-4">
      <div 
        v-for="thread in threadStore.popularThreads"
        :key="thread.id"
        class="col-md-4"
      >
    <RouterLink
        :to="{name: 'ThreadDetailView', params: {threadId:thread.id}}"
        class="text-decoration-none text-dark d-block h-100"
    >
      <div class="thread-card h-100">
        <!-- title -->
      <p class="thread-title fw-bold">“{{ thread.title }}”</p>
        <!-- 유저 이름 + 좋아요 -->
        <div class="mt-2">
          <div class="fw-semibold small text-muted">
            {{ thread.user?.username }} | 좋아요: {{ thread.like_count }}
          </div>
        </div>
      </div>
    </RouterLink> 
    </div>    
  </div>
  </div>
</template>

<script setup>
  import { useThreadStore } from '@/stores/threads'
  import {RouterLink} from 'vue-router'

  const threadStore = useThreadStore()

</script>

<style scoped>

</style>