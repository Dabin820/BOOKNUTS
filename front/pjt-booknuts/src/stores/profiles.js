// stores/profiles.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import defaultProfileImg from '@/assets/image/default_profile.png'

export const useProfileStore = defineStore('profile', () => {
  const API_URL = 'http://127.0.0.1:8000/booknuts'
  const accountStore = useAccountStore()
  const myLibrary = ref([])

  // 프로필 정보
  const getProfile = async (userPk) => {
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/profile/${userPk}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      return res.data
    } catch (err) {
      // 에러를 컴포넌트에서 핸들링할 수 있게 throw
      throw err
    }
  }


  // 프로필 이미지
  const IMAGE_URL = 'http://127.0.0.1:8000'
  const getImgUrl = function (profileImg) {
    console.log('프로필 이미지 경로:', profileImg)
    if (!profileImg) {
      return defaultProfileImg
    }
    if (profileImg.startsWith('http')) {
      console.log('✅ profileImg는 절대 URL:', profileImg)
      return profileImg
    }
    const fullUrl = `${IMAGE_URL}${profileImg}`
    console.log('✅ 상대 경로 처리 → 최종 이미지 URL:', fullUrl)

    return fullUrl
  }

  // 내 서재에 책 추가
  const addBookToLibrary = async (bookId) => {
    try {
      await axios({
        method: 'POST',
        url: `${API_URL}/profile/library/add/`,
        data: { book_id: bookId },
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      return true
    } catch (err) {
      // 에러를 컴포넌트에서 핸들링할 수 있게 throw
      throw err
    }
  }

  // 내 서재 목록 조회
  const getMyLibrary = async () => {
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/profile/library/`,
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      myLibrary.value = res.data
    } catch (err) {
      myLibrary.value = []
      throw err
    }
  }

  // 특정 유저의 서재 조회
  const getUserLibrary = async (userPk) => {
    console.log('getUserLibrary 호출, userPk:', userPk)
    try {
      const res = await axios({
        method: 'GET',
        url: `${API_URL}/profile/library/`,
        params: { user_pk: userPk },
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      console.log('서재 응답:', res.data)
      myLibrary.value = res.data
    } catch (err) {
      myLibrary.value = []
      throw err
    }
  }

  return { 
    getProfile,
    IMAGE_URL, getImgUrl,
    addBookToLibrary, getMyLibrary, myLibrary,
    getUserLibrary,
   }
}, { persist:true })
