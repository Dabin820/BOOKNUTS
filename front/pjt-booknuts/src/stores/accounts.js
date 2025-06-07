// stores/accounts.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useBookStore } from '@/stores/books'


export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref(null)
  const user = ref(null) // 유저 정보 저장
  const signUpError = ref('')  // 회원가입시 에러 메시지 상태 
  const logInError = ref('')  // 로그인시 에러 메시지 상태

  const bookStore = useBookStore()

  const isLogin = computed(() => {
    return token.value !== null && token.value !== ''
  })

  // 회원가입
  const signUp = function (payload) {
    // console.log(payload)
    const { username, email, age, password1, password2, interestedGenres, profileImg, annualReadingAmount } = payload
    const formData = new FormData()
    formData.append('username', username)
    formData.append('email', email)
    formData.append('age', age)
    formData.append('password1', password1)
    formData.append('password2', password2)
    // 장르 ID 배열을 각각 append
    interestedGenres.forEach(id => {
      formData.append('interested_genres_ids', id)
    })
    if (profileImg) formData.append('profile_img', profileImg)
    if (annualReadingAmount) formData.append('annual_reading_amount', annualReadingAmount)
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then(res => {
      // console.log('회원가입 성공!')
      // 회원가입 성공 후 자동 로그인
      signUpError.value = ''  // 성공 시 에러 초기화
      const password = password1
      logIn({ username, password })
    })
    .catch(err => {
      // 에러 메시지 추출 및 저장
      const data = err.response?.data
      if (data) {
        if (data.password1) signUpError.value = data.password1[0]
        else if (data.password2) signUpError.value = data.password2[0]
        else if (data.non_field_errors) signUpError.value = data.non_field_errors[0]
        else signUpError.value = '회원가입에 실패했습니다.'
      } else {
        signUpError.value = '회원가입에 실패했습니다.'
      }
    })
  }

  // 로그인
  const logIn = function ({ username, password }) {
    logInError.value = ''  // 로그인 시도 전 에러 초기화
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: { username, password }
    })
    .then(res => {
      token.value = res.data.key
      axios.defaults.headers.common['Authorization'] = `Token ${token.value}`

      axios({
        method: 'GET',
        url: `${ACCOUNT_API_URL}/user/`
      })
      .then(res => {
        user.value = res.data
        router.push({ name: 'MainView' })
      })
      .catch(err => {
        console.error('유저 정보 불러오기 실패:', err)
        router.push({ name: 'MainView' })
      })
    })
    .catch(err => {
      const data = err.response?.data
      if (data && data.non_field_errors) {
        // 기본 메시지면 한글로 대체
        if (data.non_field_errors[0] === "Unable to log in with provided credentials.") {
          logInError.value = "아이디 또는 비밀번호가 올바르지 않습니다."
        } else {
          logInError.value = data.non_field_errors[0]
        }
      } else if (data && data.detail) {
        logInError.value = data.detail
      } else {
        logInError.value = '로그인에 실패했습니다'
      }
    })
  }


  // 로그아웃
  const logOut = function (showConfirm = true) {
    if (showConfirm && !window.confirm('정말 로그아웃 하시겠습니까?')) {
      return
    }
    // 서버 로그아웃 먼저
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(() => {
      console.log('서버 로그아웃 성공')
    })
    .catch((err) => {
      console.warn('⚠️ 로그아웃 실패 (무시)', err)
    })
    .finally(() => {
      // 클라이언트 상태 초기화
      localStorage.removeItem('token')
      sessionStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      token.value = null
      user.value = null
      // 도서 스토어 초기화
      bookStore.$reset()
      bookStore.getBooks()

      router.push({ name: 'MainView' })
    })
  }

  // 회원 탈퇴
  const deleteAccount = async (userPk) => {
    try {
      await axios({
        method: 'DELETE',
        url: `http://127.0.0.1:8000/booknuts/profile/${userPk}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      // 탈퇴 후 로그아웃 (여기서 클라이언트 상태까지 정리됨)
      logOut(false) // showConfirm=false로 설정하여 확인 창 표시 안 함
      return true
    } catch (err) {
      console.warn('⚠️ 탈퇴 중 에러 발생')
      throw err
    }
  }

  // 회원 정보 수정
  const updateProfile = async (userInfo) => {
    console.log('🟡 [updateProfile] userInfo:', userInfo)
    console.log('🟠 user.value:', user.value)

    const formData = new FormData()
    for (const key in userInfo) {
      if (userInfo[key] !== undefined && userInfo[key] !== null) {
        if (Array.isArray(userInfo[key])) {
          userInfo[key].forEach(v => formData.append(key, v))
        } else {
          formData.append(key, userInfo[key])
        }
      }
    }
    // userPk를 store에서 가져오기 (예: user.value.pk)
    const pk = userInfo.userId || user.value?.id || user.value?.pk// css 수정하면서 오류나서 id -> pk로 수정함
    
    const res = await axios({
      method: 'PATCH',
      url: `http://127.0.0.1:8000/booknuts/profile/${pk}/`,
      data: formData,
      headers: {
        Authorization: `Token ${token.value}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log(res.data)
    user.value = res.data
  }
  


  return { 
    token, isLogin, user,
    signUp, logIn, logOut, deleteAccount, updateProfile,
    signUpError, logInError,
   }
}, { persist: true })
