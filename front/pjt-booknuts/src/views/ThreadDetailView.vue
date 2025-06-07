<!-- views/ThreadDetailView.vue -->
<template>
  <div>
    <ThreadDetail :thread="threadStore.threadDetail" />
  </div>
</template>

<script setup>
  import { onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { useThreadStore } from '@/stores/threads'
  import ThreadDetail from '@/components/ThreadDetail.vue'

  const route = useRoute()
  const threadStore = useThreadStore()

  onMounted(() => {
    // [디버깅용] console.log('ThreadId:', route.params.threadId)
    const threadId = route.params.threadId
    threadStore.getOneThread(threadId)
    threadStore.getComments(threadId)
  })
</script>

<style scoped>

</style>