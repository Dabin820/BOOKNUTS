<!-- views/ThreadEditView.vue -->
<template>
  <div>
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="error">에러: {{ error }}</div>
    <div v-else-if="thread">
        <h3 class="fw-bold  mt-3 mb-0 text-center">게시글 수정</h3>
        <ThreadCreateForm :thread="thread" :isEdit="true" />
      </div>
    </div>
</template>

<script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import { useThreadStore } from '@/stores/threads'
  import ThreadCreateForm from '@/components/ThreadCreateForm.vue'

  const route = useRoute()
  const threadStore = useThreadStore()
  const thread = ref(null)
  const loading = ref(true)
  const error = ref(null)

  const fetchThread = async (threadId) => {
  loading.value = true
    error.value = null
    try {
      thread.value = await threadStore.getOneThread(threadId)
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    fetchThread(route.params.threadId)
  })

  watch(
    () => route.params.threadId,
    (newId, oldId) => {
      if (newId !== oldId) {
        fetchThread(newId)
      }
    }
  )
</script>

<style scoped>
</style>
