// stores/books.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import Fuse from 'fuse.js'

export const useBookStore = defineStore('book', () => {
  const API_URL = 'http://127.0.0.1:8000/booknuts'
  const books = ref([])
  const selectedCategory = ref('all')
  const selectedBook = ref(null)
  const searchQuery = ref('')
  const currentPage = ref(1)
  const pageSize = 9


  // 전체 도서 조회
  const getBooks = function(){
    const params = {}
    if (selectedCategory.value !== 'all') {
      params.category = selectedCategory.value 
    }
    axios({
      method:'get',
      url:`${API_URL}/books/`,
      params: params 
    })
    .then(res=>{
      books.value = res.data 
      currentPage.value = 1
    })
    .catch(err=> {
      console.log(err)
    })
  }
  
  // 베스트셀러 ISBN 리스트
  const bestsellerIsbnList = [
    "9788936434120",  // 소년이 온다
    "9788954682152",  // 작별하지 않는다
    "9788936434595",  // 채식주의자 (리마스터판)
    "9788954651134",  // 흰
    "9788932020006",  // 바람이 분다, 가라
    "9788954616515",  // 희랍어 시간
    "9788932034812",  // 여수의 사랑
    "9788932034829",  // 내 여자의 열매
    "9788932024639",  // 서랍에 저녁을 넣어 두었다
    "9788954693462",   // 디 에센셜 한강 (무선 보급판)
    "9788998441012",  // 모순 - 개정판
    "9788925554990", // 스토너
    "9791162203620", // 파과
    "9788937473401", // 급류
  ]
  const bestsellers = computed(() => {
    return books.value
      // 1. 해당 ISBN만 필터링
      .filter(book => bestsellerIsbnList.includes(book.isbn))
      // 2. 정렬: 리뷰 순위 → 출간일 최신순
      .sort((a, b) => {
        if (b.customer_review_rank !== a.customer_review_rank) {
          return b.customer_review_rank - a.customer_review_rank
        }
        return new Date(b.pub_date) - new Date(a.pub_date)
      })
      // 3. 상위 8권만 반환
      .slice(0, 12)
  })
  
  // book조회- 검색어 필터링(Fuse.js기반)
  const filteredBooks = computed(() => {
    if (!searchQuery.value) return books.value
    const options = {
      keys: [
        'title',
        'author',
        'description',
      ],
      threshold: 0.4,
    }
    const fuse = new Fuse(books.value, options)
    return fuse.search(searchQuery.value).map(result => result.item)
  })

  // 페이지 보여주기 
  const paginatedBooks = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredBooks.value.slice(start, start + pageSize)
  })

  //전체 페이지수 
  const totalPages = computed(() => {
    return Math.ceil(filteredBooks.value.length / pageSize)
  })

  // 일부 도서 조회 
  const getBookDetail = function(bookId){
    axios({
      method:'get',
      url:`${API_URL}/books/${bookId}/`,
    })
    .then((res) =>{
      console.log(res.data)
      selectedBook.value=res.data
      return res.data
    })
    .catch((err)=>{
      console.log(err)
    })
  }

  // 상태 초기화 함수 - 필요한 모든 페이지 초기화
  const $reset = function ()  {
    books.value = []
    selectedCategory.value = 'all'
    selectedBook.value = null
    searchQuery.value = ''
    currentPage.value = 1
  }


  return { 
    API_URL,
    books,
    bestsellers,
    selectedCategory,
    searchQuery,
    currentPage,
    pageSize,
    getBooks,
    
    filteredBooks,
    paginatedBooks,
    totalPages,
    getBookDetail,
    selectedBook,
    $reset,
   }
})
