<template>
  <div class="thread-card p-3 rounded shadow-sm h-100" @click="goToDetail" style="cursor: pointer;">
    <img :src="getCoverImgUrl(thread.cover_img || thread.book.cover)" alt="cover" class="img-fluid rounded mb-3" />
    <p class="thread-title fw-bold">“{{ thread.title }}”</p>

    <!-- 작성자 정보 -->
    <div class="d-flex align-items-center mt-2 gap-2">
      <img
        :src="getImgUrl(thread.user.profile_img)"
        alt="작성자 이미지"
        class="rounded-circle"
        style="width: 30px; height: 30px; object-fit: cover;"
      />
      <small class="text-muted">{{ thread.user.username }}</small>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profiles'
import {useThreadStore} from '@/stores/threads'

const router = useRouter()
const profileStore = useProfileStore()
const threadStore = useThreadStore()

const props = defineProps({
  thread: Object,
})

const getImgUrl = profileStore.getImgUrl
const getCoverImgUrl = threadStore.getCoverImgUrl

const goToDetail = () => {
  router.push({ name: 'ThreadDetailView', params: { threadId: props.thread.id } })
}
</script>
