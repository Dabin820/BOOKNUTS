<!-- views/ThreadCreateForm.vue -->
<template>
  <div class="container py-5">
    <LoadingSpinner v-if="isLoading" />
    <div class="p-5 rounded" style="background-color: #f5e9dc;">
      <!-- thread 생성 폼 -->
      <form @submit.prevent="onSubmit">
        <!-- 한줄평 -->
        <div class="row mb-4 align-items-start">
          <label for="title" class="col-md-3 col-form-label fw-bold">한줄평</label>
          <div class="col-md-9">
            <textarea
              id="title"
              class="form-control"
              v-model.trim="title" required
              placeholder="한줄평을 입력하세요"
              maxlength="100"
              rows="2"  
            ></textarea>
          </div>
        </div>
        
        <div class="row mb-4 align-items-start">
          <label for="content" class="col-md-3 col-form-label fw-bold">내용</label>
          <div class="col-md-9">
            <textarea
              id="content"
              class="form-control"
              v-model.trim="content" required
              placeholder="내용을 입력하세요"
              rows="10"
              ></textarea>
          </div>
        </div>
        
        <div class="row mb-5 align-items-center">
          <label for="readingDate" class="col-md-3 col-form-label fw-bold">읽은 날짜</label>
          <div class="col-md-4">
            <input 
              id="readingDate"
              type="date"
              class="form-control"
              v-model="readingDate" required
              placeholder="읽은 날짜를 선택하세요"
            >
            <span v-if="!readingDate" class="text-danger small">읽은 날짜를 선택하세요</span>
          </div>
        </div>

        <div class="d-flex justify-content-between mt-4">
          <button type="button" class="btn btn-outline-dark px-4" @click="onCancel">종료</button>
          <button type="submit" class="btn btn-warning px-4" :disabled="!canSave">{{ isEdit ? '수정' : '작성'}}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useThreadStore } from '@/stores/threads'
  import LoadingSpinner from './LoadingSpinner.vue'

  const isLoading = ref(false)
  const router = useRouter()
  const threadStore = useThreadStore()
  const props = defineProps({
    // book: {
    //   type: Object,
    //   required: true
    // },
    book: Object,
    thread: Object,
    isEdit: Boolean, // true이면 수정 모드
  })
  
  // 초기값: 수정이면 thread에서, 아니면 빈 값
  const title = ref(props.thread?.title || '')
  const content = ref(props.thread?.content || '')
  const readingDate = ref(props.thread?.reading_date || '')

  // thread prop이 바뀔 때도 값 동기화
  watch(() => props.thread, (newThread) => {
    if (newThread) {
      title.value = newThread.title
      content.value = newThread.content
      readingDate.value = newThread.reading_date
    }
  })

  const canSave = computed(() => {
    return title.value && content.value && readingDate.value
  })

  const onSubmit = async () => {
    // 입력값 검증: 읽은 날짜가 비어있으면 경고 후 리턴
    if (!canSave.value) return
    isLoading.value = true 
    try {
      if (props.isEdit) {
        await threadStore.updateThread({
          threadId: props.thread.id,
          title: title.value,
          content: content.value,
          reading_date: readingDate.value,
        })
        alert('Thread 수정 완료!')
        router.push({ name: 'ThreadDetailView', params: { threadId: props.thread.id } })
        return  // 페이지 이동 후 아래 코드 실행 방지
      } else {
        const thread = await threadStore.createThread({
          title: title.value,
          content: content.value,
          reading_date: readingDate.value,
          book: props.book,
        })
        alert('Thread 작성 완료!')
        router.push({ name: 'ThreadDetailView', params: { threadId: thread.id } })
        return  // 페이지 이동 후 아래 코드 실행 방지
      }
    } catch (e) {
      alert(props.isEdit ? 'Thread 수정에 실패했습니다.' : 'Thread 작성에 실패했습니다.')
      isLoading.value = false  // 실패한 경우만 로딩 종료
      onClear()                // 실패한 경우만 폼 초기화
    }
  }
  
  // 종료 버튼 핸들러
  const onCancel = () => {
    if (props.isEdit) {
      // 수정 모드: Thread 상세 페이지로 이동
      router.push({ name: 'ThreadDetailView', params: { threadId: props.thread.id } })
    } else {
      // 생성 모드: 책 상세 페이지로 이동
      if (props.book?.id) {
        router.push({ name: 'BookDetailView', params: { bookId: props.book.id } })
      } else {
        // book 정보가 없으면 이전 페이지로
        router.go(-1)
      }
    }
  }

  // 폼 초기화 함수
  const onClear = () => {
    title.value = ''
    content.value = ''
    readingDate.value = ''
  }
</script>


<style scoped>

</style>