<!-- views/ThreadDetail.vue -->
<template>
  <div v-if="thread" class="container py-5">
    <div class="row">
      <!-- Thread 내용 -->
      <!-- 좌측: 본문/작성자/날짜/좋아요 -->
      <div class="col-md-8">
        <div class="mb-4">
          <!-- 본문 -->
          <blockquote class="fs-5 text-muted border-start border-4 ps-3 mb-3">
            한줄평
          </blockquote>
          <h3 class="fw-bold">{{ thread.title }}</h3>
          <div class="mt-3">{{ thread.content }}</div>
        </div>

        <!-- 유저 영역 -->
        <div class="d-flex align-items-center mb-4">
          <!-- 프로필 이미지 -->
          <RouterLink
            :to="{ name:'ProfileView', params:{ userPk: thread.user.id } }"
          >
          <div>
            <img :src="profileStore.getImgUrl(thread.user.profile_img)" alt="profileImg" width="48" height="48" class="rounded-circle me-3" />
          </div>
          </RouterLink>
          
          <!-- 작성일 -->
          <div>
            <div class="fw-semibold">{{ thread.user.username }}</div>
            <div class="text-muted small">
              작성일: {{ thread.reading_date || (thread.created_at && thread.created_at.slice(0, 10)) }}
            </div>
          </div>
        </div>

        <!-- 좋아요 -->
        <div class="mb-5">
          <button class="btn px-3" :class="isLiked ? 'btn-danger' : 'btn-outline-dark'" @click="onLike">
              {{ isLiked ? '♥' : '♡' }}
          </button>
          <div class="ms-2">좋아요 {{ likeCount }}</div>
        </div>
      </div>

      <!-- 우측 영역  -->
       <div class="col-md-4">
        <!-- 나중에 쓰레드 이미지 커버 들어올 자리 -->
        <div v-if="thread" class="mb-4 bg-light rounded d-flex align-items-center justify-content-center" style="height: 280px;">
          <div v-if="thread.cover_img" class="mb-4">
            <img :src="getCoverImgUrl(thread.cover_img)" alt="Thread Cover" class="img-fluid rounded" />
          </div> 
        </div>
        <!-- 도서 정보 카드  -->
        <div class="card p-3 shadow-sm">
          <div class="row g-0">
            <div class="col-4">
              <RouterLink
                :to="{ name: 'BookDetailView', params: { bookId: thread.book.isbn } }"
                class="text-decoration-none text-dark">
              <img :src="thread.book.cover" alt="cover" class="img-fluid rounded-start" />
              </RouterLink>    
            </div>
            <div class="col-8">
              <div class="card-body">
                <p class="card-title fw-bold mb-1 fs-6">{{ thread.book.title }}</p>
                <p class="card-text small text-muted mb-0">{{ thread.book.author }}</p>
              </div>
            </div>
          </div>
        </div>
       </div>
    </div>

    <!-- 댓글 영역: 본문 하단 -->
    <div class="mt-4 border-top pt-4">
      <h4 class="fw-bold mb-3"><i class="bi bi-chat-left-text"></i>  댓글</h4>
      <form class="d-flex mb-3" @submit.prevent="onCreateComment">
        <input v-model.trim="commentInput" class="form-control me-2" placeholder="댓글을 입력하세요" maxlength="100" required />
        <button class="btn btn-warning" type="submit">등록</button>
      </form>
      <div v-if="threadStore.isCommentLoading">댓글 불러오는 중...</div>
      <div v-for="comment in comments" :key="comment.id" class="d-flex align-items-center justify-content-between border rounded p-2 mb-2">
        <div>
          <span class="me-3"><strong>{{ comment.user.username }}</strong></span>
          <span>{{ comment.content }}</span>
        </div>
        <div>
          <button @click="onDeleteComment(comment.id)" class="btn btn-sm btn-outline-secondary">댓글 삭제</button>
        </div>
      </div>
      <div v-if="!threadStore.isCommentLoading && comments.length === 0" class="text-muted">
        <span>아직 댓글이 없습니다</span>
      </div>
    </div>
  </div>
  <div v-else>
    <p>로그인이 필요합니다!</p>
  </div>
    
</template>


<script setup>
  import { ref, watchEffect, onMounted, computed } from 'vue'
  import { useRoute, RouterLink } from 'vue-router'
  import { useThreadStore } from '@/stores/threads'
  import { useAccountStore } from '@/stores/accounts'
  import BookCard from './BookCard.vue'
  import {useProfileStore} from '@/stores/profiles'

  const threadStore = useThreadStore()
  const accountStore = useAccountStore()
  const profileStore = useProfileStore()
  const getCoverImgUrl = threadStore.getCoverImgUrl
  const route = useRoute()

  const threadId = computed(() => {
    return route.params.threadId
  })
  const comments = computed(() => threadStore.comments[threadId.value] || [])

  const props = defineProps({
    thread: {
      type: Object,
      default: () => null,
    },
  })
  const thread = computed(() => props.thread) 
  // 좋아요 상태와 수
  const isLiked = ref(false)
  const likeCount = ref(0)

  // 좋아요 상태 (프론트에서 관리)
  watchEffect(() => {
    const newThread = props.thread
    if (newThread) {
      likeCount.value = newThread.like_count || 0
      isLiked.value = newThread.is_liked || false
    } else {
      likeCount.value = 0
      isLiked.value = false
    }
  })

const onLike = async () => {
  try {
    // 좋아요 상태와 관계없이 toggle 요청
    const res = await threadStore.toggleLike(props.thread.id)
    likeCount.value = res.like_count
    isLiked.value = res.liked
  } catch (e) {
    alert('본인 게시물은 좋아요를 누를 수 없어요!')
  }
}

  // 프로필 이미지
  const IMAGE_URL = 'http://127.0.0.1:8000'
  const getImgUrl = function (profileImg) {
    if (!profileImg) {
      return ''
    }
    if (profileImg.startsWith('http')) {
      return profileImg
    }
    return IMAGE_URL + profileImg
  }

  // 댓글
  const commentInput = ref('')

  onMounted(() => {
    // console.log('props.thread:', props.thread)
    if (props.thread) {
    threadStore.getComments(props.thread.id)
  }
  })

  const onCreateComment = async () => {    
    // console.log('댓글 등록 시도:', props.thread.id, commentInput.value)
    if (!commentInput.value.trim()) return
    const ok = await threadStore.createComment(props.thread.id, commentInput.value)
    if (ok) commentInput.value = ''
  }

  const onDeleteComment = async (commentId) => {
    try {
      await threadStore.deleteComment(commentId, props.thread.id)
    } catch (err) {
      if (err.response && err.response.status === 403) {
        alert('본인 댓글만 삭제할 수 있습니다!')
    } else {
        alert('댓글 삭제 중 오류가 발생했습니다.')
      }
    }
  }

</script>


<style scoped>
</style>