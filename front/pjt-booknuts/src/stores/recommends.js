// stores/recommends.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useRecommendStore = defineStore('recommend', () => {
  const API_URL = 'http://127.0.0.1:8000/booknuts'
  const recommendations = ref([]) // AI 추천을 위한 상태
  const itemBasedRecommendations = ref([]) // 아이템 기반 추천을 위한 상태
  const loading = ref(false)
  const error = ref(null)
  

  // 책 추천 요청을 처리하는 함수
  const fetchRecommendations = async (query) => {
    loading.value = true
    error.value = null
    recommendations.value = []  // 초기화
    try {
      const res = await axios({
        method: 'POST',
        url: `${API_URL}/books/recommend/`,
        data: { query },
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 5000, // 5초 타임아웃 설정
      })
      recommendations.value = res.data
    } catch (err) {
      error.value = err.response?.data?.error || '추천 요청 실패'
    } finally {
      loading.value = false
    }
  }

  // 추천 목록을 초기화하는 함수
  const clearRecommendations = function () {
    recommendations.value = []
    error.value = null
  }

  // 아이템 기반 추천 요청 함수
  const fetchItemBasedRecommendations = async (bookId) => {
    loading.value = true
    error.value = null
    itemBasedRecommendations.value = []  // 초기화
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/books/${bookId}/item-recommend/`,
        timeout: 5000, // 5초 타임아웃 설정
      })
      console.log('아이템 기반 추천 응답:', res.data) // 디버깅용 로그
      itemBasedRecommendations.value = res.data
    } catch (err) {
      error.value = err.response?.data?.error || '아이템 기반 추천 요청 실패'
      console.error('추천 에러:', error.value)
    } finally {
      loading.value = false
    }
  }

  return { 
    recommendations, loading, error,
    fetchRecommendations, clearRecommendations,
    fetchItemBasedRecommendations, itemBasedRecommendations,
   }
}, { persist: true })
