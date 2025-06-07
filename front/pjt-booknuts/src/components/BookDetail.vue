<!-- components/BookDetail.vue -->
<template>
  <div v-if="book">
      <!-- ✅ 추가: 내 서재 버튼 -->
    <div class="container text-end my-3">
      <button class="btn btn-outline-primary" @click="onAdd">📚 내 서재에 담기</button>
    </div>
    <!-- 도서 상세 정보 섹션 -->
    <section class="book-info-section py-5">
      <div class="container">
        <div class="row">
          <!-- 왼쪽: 도서 설명 -->
          <div class="col-md-7">
            <div class="book-text">
              <h1 class="book-title">{{ book.title }}</h1>
              <p class="text-muted mb-4">책 소개</p>
              <p class="description">{{ book.description }}</p>

              <div class="mt-4">
                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="card shadow-sm rounded p-3 h-100" style="background-color: #fff4e2;">
                      <div class="d-flex align-items-center">
                        <i class="bi bi-building fs-4 me-2 text-secondary"></i>
                        <div>
                          <div class="fw-semibold mb-1">출판사:</div>
                          <div class="text-muted">{{ book.publisher }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card shadow-sm rounded p-3 h-100" style="background-color: #fff4e2;">
                      <div class="d-flex align-items-center">
                        <i class="bi bi-calendar fs-4 me-2 text-secondary"></i>
                        <div>
                          <div class="fw-semibold mb-1">출간일:</div>
                          <div class="text-muted">{{ book.pub_date }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 오른쪽: 도서 커버 및 작가 정보 -->
          <div class="col-md-5 text-center">
            <img :src="book.cover" :alt="book.title" class="img-fluid shadow-sm rounded book-cover-img mb-3" />
            <div class="author-card text-start p-3 rounded">
              <h5 class="fw-bold mb-3">작가 정보</h5>
              <div class="d-flex align-items-start">
                <img
                  :src="book.author_photo"
                  alt="author"
                  class="rounded-circle me-3"
                  style="width: 48px; height: 48px; object-fit: cover"
                />
                <div>
                  <div class="fw-bold">{{ book.author }}</div>
                  <div class="text-muted small author-info-truncate">{{ book.author_info }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 추천/스레드/지도 통합 섹션 -->
    <section class="container py-5">
      <!-- 왼쪽: Thread 목록 -->
      <div class="mb-5">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="fw-bold mb-3">이 책의 Threads</h3>
          <button class="btn btn-outline-warning btn-sm"@click="goToCreateThread">Thread 생성하기</button>
        </div>
        
        <div class="row g-3">
          <div
              v-for="thread in threadStore.threadsByBook"
              :key="thread.id"
              class="col-md-6"
            >
            <RouterLink
              :to="{ name: 'ThreadDetailView', params: { threadId: thread.id }}"
              class="text-decoration-none text-dark"
            >
            <div class="thread-card p-3 h-100">
              <p class="fw-bold mb-2">{{ thread.title }}</p>
              <img :src="profileStore.getImgUrl(thread.user.profile_img)" alt="profileImg" width="50px" />
              <p class="text-muted mb-0 small">{{ thread.user.username }}</p>
            </div>
          </RouterLink>
          </div>
        </div>
        <div v-if="threadStore.threadsByBook.length === 0">
            <span class="text-muted">아직 작성된 Thread가 없습니다</span>
        </div>
      </div>

      <hr>

      <!-- 오른쪽: 추천 + 지도 -->
      <div class="row d-flex align-items-stretch">
        <div class="col-md-6 mb-4 h-100">
          <h3 class="fw-bold">함께 읽으면 더 좋아요📚</h3>
          <Recommendations />
        </div>
        <div class="col-md-6 mb-4 h-100">
          <h3 class="fw-bold">이 책 어디서 보지?📍</h3>
          <GoogleMaps />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted,watch } from 'vue'
import { useRoute,useRouter } from 'vue-router'
import { useBookStore } from '@/stores/books'
import {useThreadStore} from '@/stores/threads'
import {useProfileStore} from '@/stores/profiles'
import {useAccountStore} from '@/stores/accounts'
import ThreadList from './ThreadList.vue'
import Recommendations from './Recommendations.vue'
import GoogleMaps from './GoogleMaps.vue'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()

const bookStore = useBookStore()
const threadStore = useThreadStore()
const profileStore = useProfileStore()
const accountStore = useAccountStore()
const { selectedBook: book } = storeToRefs(bookStore)
const {threadsByBook} = storeToRefs(threadStore)

// Thread 생성 버튼 핸들러
const goToCreateThread = () => {
  router.push({
    name: 'ThreadCreateView',
    params: { bookId: route.params.bookId },
  })
}
// onMounted(() => {
//   bookStore.getBookDetail(route.params.bookId)
//   threadStore.getThreadsByBook(route.params.bookId)
// })

// ✅ 내 서재 담기 기능
const onAdd = async () => {
  if (!accountStore.isLogin) {
    const goLogin = confirm('로그인이 필요합니다.\n로그인 페이지로 이동할까요?')
    if (goLogin) {
      router.push({ name: 'LogInView' })
    }
    return
  }

  try {
    await profileStore.addBookToLibrary(route.params.bookId)
    // 책 추가 성공 후 서재 목록 갱신
    await profileStore.getMyLibrary()
    const goProfile = confirm('내 서재에 담았습니다!\n내 프로필 페이지에서 확인하시겠어요?')
    if (goProfile) {
      router.push({ name: 'ProfileView', params: { userPk: accountStore.user?.id } })
    }
  } catch (err) {
    if (
      err.response &&
      err.response.data &&
      err.response?.data?.detail === '이미 내 서재에 담긴 책입니다.'
    ) {
      const goProfile = confirm('이미 내 서재에 담긴 책입니다!\n내 프로필 페이지에서 확인하시겠어요?')
      if (goProfile) {
        router.push({ name: 'ProfileView', params: { userPk: accountStore.user?.id } })
      }
    } else {
      alert('오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
    }
  }
}

// 최초 마운트 시
onMounted(async () => {
  await bookStore.getBookDetail(route.params.bookId)
  await threadStore.getThreadsByBook(route.params.bookId)
})


// bookId가 바뀔 때마다 새로 fetch
watch(
  () => route.params.bookId,
  async (newBookId) => {
    await bookStore.getBookDetail(newBookId)
    await threadStore.getThreadsByBook(newBookId)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
)

</script>

<style scoped>
@import "@/assets/styles/global.css";
</style>
