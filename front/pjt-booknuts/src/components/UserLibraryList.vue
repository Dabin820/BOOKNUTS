<!-- views/UserLibraryList.vue -->
<template>
  <section class="mb-5">
    <h4 class="fw-bold mb-4">나의 서재</h4>
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="error" class="text-danger">에러: {{ error }}</div>
    <div v-else>
      <div v-if="books.length === 0">아직 추가한 책이 없습니다.</div>
      <div class="d-flex flex-wrap gap-3">
        <div
          v-for="item in books"
          :key="item.id"
          class="book-cover-card"
          @click="goToBookDetail(item.book.isbn)"
        >
          <img
            :src="profileStore.getImgUrl(item.book.cover)"
            alt="표지"
            class="rounded shadow-sm"
            style="width: 120px; height: 180px; object-fit: cover; cursor: pointer;"
          />
        </div>
      </div>
    </div>
  </section>
</template>


<script setup>
  import  { ref, onMounted, watch } from 'vue'
  import { useProfileStore } from '@/stores/profiles'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const profileStore = useProfileStore()

  const props = defineProps({
    userPk: {
      type: [Number, String],
      required: true
    }
  })

  const books = ref([])
  const loading = ref(true)
  const error = ref(null)

  // 유저의 서재를 가져오는 함수
  const fetchLibrary = async () => {
    loading.value = true
    error.value = null
    try {
      await profileStore.getUserLibrary(props.userPk)
      // console.log('myLibrary:', profileStore.myLibrary)
      books.value = profileStore.myLibrary
      // console.log('books:', books.value)
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  // 책 상세 페이지로 이동하는 함수
  const goToBookDetail = (isbn) => {
    router.push({ name: 'BookDetailView', params: { bookId: isbn } })
  }

  onMounted(fetchLibrary)
  watch(() => props.userPk, fetchLibrary)

</script>
