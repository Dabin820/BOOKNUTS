// stores/threads.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import Fuse from 'fuse.js'
import { useAccountStore } from '@/stores/accounts'


export const useThreadStore = defineStore('thread', () => {
  const API_URL = 'http://127.0.0.1:8000/booknuts'
  const threads = ref([])
  const selectedCategory = ref('all')
  const searchQuery = ref('')
  const currentPage = ref(1)
  const pageSize = 9
  const threadDetail = ref(null)
  const comments = ref({})
  const isCommentLoading = ref(false)


  // thread 조회 - 서버 필터링 (카테고리별)
  const getThreads = async () => {
    const params = {}
    if (selectedCategory.value && selectedCategory.value !== 'all') {
      params.category = selectedCategory.value
    }
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/threads/`,
        params: params
      })
      // console.log('API 응답:', res.data)
      threads.value = res.data
    } catch (err) {
      console.log(err)
    }
  }

  // thread 조회 - 검색어 필터링 (Fuse.js 기반)
  const filteredThreads = computed(() => {
    // 검색어 없으면 전체 반환
    if (!searchQuery.value) return threads.value
    const options = {
      keys: [
        'book.author',
        'book.title',
        'book.description',
        'title',    // 쓰레드 제목
        'content',  // 쓰레드 내용
        'user.username',     // 쓰레드 작성자
      ],
      threshold: 0.4,
    }
    const fuse = new Fuse(threads.value, options)
    return fuse.search(searchQuery.value).map(result => result.item)
  })

  // thread 조회 - 세부내용
  const getOneThread = async function (threadId) {
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/threads/${threadId}/`,
      })
      threadDetail.value = res.data
      return res.data
    } catch (err) {
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        alert('로그인이 필요합니다.')
        threadDetail.value = null
      } else {
        alert('스레드 정보를 불러오지 못했습니다.')
        threadDetail.value = null
      }
      throw err
    }
  }

  // thread 조회 - thread preview by book
  const threadsByBook = ref([])  // 책별 스레드 미리보기 저장소
  const getThreadsByBook = async (bookId) => {
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/books/${bookId}/threads-preview/`
      })
      threadsByBook.value = res.data
    } catch (err) {
      threadsByBook.value = []
      console.error('이 책의 thread 목록 조회 실패:', err)
    }
  }

  // thread 생성
  const createThread = async (payload) => {
    const accountStore = useAccountStore()
    const { title, content, reading_date, book } = payload
    try {
      const res = await axios({
        method: 'POST',
        url: `${API_URL}/books/${book.isbn}/threads/`,
        data: { title, content, reading_date },
        headers: {
          'Authorization': `Token ${accountStore.token}`
        }
      })
      // 필요하다면 threads.value.unshift(res.data)
      console.log('생성된 thread 응답:', res.data)
      return res.data
    } catch (err) {
      console.log(err)
      throw err
    }
  }
  
  // +쓰레드 ai cover 생성용 
  const IMAGE_URL = 'http://127.0.0.1:8000'

  const getCoverImgUrl = (coverImgPath) => {
    if (!coverImgPath) return ''  // 또는 기본 이미지 대체 가능
    if (coverImgPath.startsWith('http')) return coverImgPath
    const url = `${IMAGE_URL}${coverImgPath}`
    console.log('[DEBUG] 최종 이미지 URL:', url)       // ✅ 최종 결과 확인
    return url
  }

  // thread 수정
  const updateThread = async ({ threadId, title, content, reading_date }) => {
    const accountStore = useAccountStore()
    try {
      const res = await axios({
        method: 'PUT',
        url: `${API_URL}/threads/${threadId}/`,
        data: { title, content, reading_date },
        headers: {
          'Authorization': `Token ${accountStore.token}`
        }
      })
      // 필요하다면 threads.value에서 해당 thread를 갱신
      return res.data
    } catch (err) {
      console.error('Thread 수정 실패:', err)
      throw err
    }
  }

  // thread 삭제
  const deleteThread = async (threadId) => {
    const accountStore = useAccountStore()
    try {
      await axios({
        method: 'DELETE',
        url: `${API_URL}/threads/${threadId}/`,
        headers: {
          'Authorization': `Token ${accountStore.token}`
        }
      })
      // threads.value에서 해당 thread를 제거(리스트 최신화)
      threads.value = threads.value.filter(t => t.id !== threadId)
      return true
    } catch (err) {
      console.error('Thread 삭제 실패:', err)
      throw err
    }
  }

  // 페이지별
  const paginatedThreads = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredThreads.value.slice(start, start+pageSize)
  })

  const totalPages = computed(() => {
    return Math.ceil(filteredThreads.value.length/pageSize)
  })

  // 좋아요
  const toggleLike = async (threadId) => {
    const accountStore = useAccountStore()
    try {
      const res = await axios({
        method: 'POST',
        url: `${API_URL}/threads/${threadId}/like/`,
        headers: {
          'Authorization': `Token ${accountStore.token}`
        },
        data: {}  // POST이므로 data는 비워둡니다(필요시 추가)
      })
      // 좋아요 상태와 수만 반환
      return res.data  // { liked, like_count }
    } catch (err) {
      console.log(err)
      throw err
    }
  }

  // 인기 쓰레드: 좋아요 수 내림차순, 같으면 생성일 내림차순, 상위 6개
  const popularThreads = computed(() => {
    // created_at이 ISO 문자열이라고 가정
    return [...threads.value]
      .sort((a, b) => {
        if (b.like_count !== a.like_count) {
          return b.like_count - a.like_count
        }
        // like_count가 같으면 created_at 내림차순
        return new Date(b.created_at) - new Date(a.created_at)
      })
      .slice(0, 6)
  })

  // 댓글 조회
  const getComments = async (threadId) => {
    isCommentLoading.value = true
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/threads/${threadId}/comments/`
      })
      comments.value[threadId] = res.data
    } catch (err) {
      comments.value[threadId] = []
      console.log('댓글 조회 실패:', err)
    } finally {
      isCommentLoading.value = false
    }
  }

  // 댓글 생성
  const createComment = async (threadId, content) => {
    const accountStore = useAccountStore()
    try {
      await axios({
        method: 'POST',
        url: `${API_URL}/threads/${threadId}/comments/`,
        data: { content },
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      // 새 댓글 등록 후 목록 갱신
      await getComments(threadId)
      return true
    } catch (err) {
      console.error('댓글 등록 실패:', err)
      return false
    }
  }

  // 댓글 삭제
  const deleteComment = async (commentId, threadId) => {
    const accountStore = useAccountStore()
    try {
      await axios({
        method: 'DELETE',
        url: `${API_URL}/comments/${commentId}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      // 삭제 후 목록 갱신
      await getComments(threadId)
      return true
    } catch (err) {
      console.error('댓글 삭제 실패:', err)
      throw err // 에러를 컴포넌트에서 핸들링할 수 있게
    }
  }


  return { 
    API_URL,
    threads, selectedCategory, searchQuery, filteredThreads, threadDetail,
    getThreads, getOneThread, createThread, updateThread, deleteThread,
    currentPage, pageSize, paginatedThreads, totalPages,
    toggleLike,
    popularThreads,
    comments, getComments, createComment, deleteComment, isCommentLoading,
    threadsByBook, getThreadsByBook,getCoverImgUrl,
   }
}, { persist:true })
