<!-- views/ThreadList.vue -->
<template>
  <div>
    <ThreadItem 
      v-for="thread in threads"
      :key="thread.id"
      :thread="thread"
      @click="goToDetail(thread.id)"
      style="cursor:pointer"
    />
  </div>

</template>


<script setup>
  import ThreadItem from './ThreadItem.vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()

  const props = defineProps({
    threads: Array,
  })

  const goToDetail = function (threadId) {
    router.push({ name: 'ThreadDetailView', params: { threadId: threadId}})
  }


</script>

<style scoped>

</style>