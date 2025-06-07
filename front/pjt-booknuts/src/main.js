// views/main.js
import '@/assets/styles/global.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'bootstrap-icons/font/bootstrap-icons.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'
import axios from 'axios'

// 앱 초기화
const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)  // ✅ persist plugin 추가

app.use(pinia)
app.use(router)

// ✅ 로그인 복구 로직: token이 있으면 헤더 설정 + 유저 정보 fetch
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

if (accountStore.token) {
  axios.defaults.headers.common['Authorization'] = `Token ${accountStore.token}`

  if (!accountStore.user) {
    axios({
      method: 'GET',
      url: 'http://127.0.0.1:8000/accounts/user/',
    })
      .then(res => {
        accountStore.user = res.data
      })
      .catch(err => {
        console.error('🔥 로그인 정보 복구 실패:', err)
        accountStore.logOut()
      })
  }
}

app.mount('#app')

