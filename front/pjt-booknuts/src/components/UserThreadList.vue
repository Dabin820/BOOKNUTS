<template>
  <section>
    <h4 class="fw-bold mb-4">내가 작성한 Threads</h4>
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="error" class="text-danger">에러: {{ error }}</div>
    <div v-else>
      <div v-if="threads.length === 0">아직 작성한 Thread가 없습니다.</div>
      <div class="vstack gap-3 mb-5">
        <div
          v-for="thread in threads"
          :key="thread.id"
          class="card shadow-sm p-3"
        >
          <div class="mb-2" @click="goToThreadDetail(thread.id)" style="cursor: pointer;">
            <strong>"{{ thread.title }}"</strong>
          </div>
          <div class="d-flex align-items-center mb-2">
            <img
              :src="profileStore.getImgUrl(thread.user.profile_img)"
              alt="profileImg"
              class="rounded-circle me-2"
              width="30"
              height="30"
              style="object-fit: cover"
            />
            <small class="text-muted">{{ thread.user.username }}</small>
          </div>
          <div class="d-flex justify-content-between">
            <button
              v-if="isMine(thread)"
              class="btn btn-warning btn-sm"
              @click="onEditThread(thread.id)"
            >
              게시글 수정
            </button>
            <button
              v-if="isMine(thread)"
              class="btn btn-outline-secondary btn-sm"
              @click.stop="onDeleteThread(thread.id)"
            >
              게시글 삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
  import axios from 'axios'
  import { ref, onMounted, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'
  import { useProfileStore } from '@/stores/profiles'
  import { useThreadStore } from '@/stores/threads'

  const router = useRouter()
  const accountStore = useAccountStore()
  const profileStore = useProfileStore()
  const threadStore = useThreadStore()

  const props = defineProps({
    userPk: {
      type: [Number, String],
      required: true
    }
  })

  const threads = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchThreads = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await axios({
        method: 'GET',
        url: 'http://127.0.0.1:8000/booknuts/threads/',
        params: { user_pk: props.userPk }
      })
      threads.value = res.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  const goToThreadDetail = (threadId) => {
    router.push({ name: 'ThreadDetailView', params: { threadId } })
  }

  const isMine = (thread) => {
    return Number(accountStore.user?.pk) === Number(thread.user?.id)
  }

  const onEditThread = (threadId) => {
    router.push({ name: 'ThreadEditView', params: { threadId } })
  }

  const onDeleteThread = async (threadId) => {
    if (!confirm('정말 삭제하시겠습니까?\n삭제 후에는 복구할 수 없습니다')) return
    try {
      await threadStore.deleteThread(threadId)
      // 삭제 후 목록 새로고침
      await fetchThreads()
      alert('게시글이 삭제되었습니다.')
    } catch (err) {
      alert('게시글 삭제에 실패했습니다.')
    }
  }

  onMounted(fetchThreads)
  watch(() => props.userPk, fetchThreads)
</script>


<style scoped>
</style>