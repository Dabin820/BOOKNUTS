// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ThreadListView from '@/views/ThreadListView.vue'
import ThreadDetailView from '@/views/ThreadDetailView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import { useAccountStore } from '@/stores/accounts'
import ThreadCreateView from '@/views/ThreadCreateView.vue'
import BookListView from '@/views/BookListView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ThreadEditView from '@/views/ThreadEditView.vue'
import UserEditView from '@/views/UserEditView.vue'
import RecommendFormView from '@/views/RecommendFormView.vue'
import RecommendView from '@/views/RecommendView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView,
    },
    {
      path: '/books/',
      name: 'BookListView',
      component: BookListView,
    },
     {
      path: '/books/:bookId',
      name: 'BookDetailView',
      component: BookDetailView,
      props: true,  // isbn을 props로 넘기기
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView,
    },
    {
      path: '/threads',
      name: 'ThreadListView',
      component: ThreadListView,
    },
    {
      path: '/threads/:threadId',
      name: 'ThreadDetailView',
      component: ThreadDetailView,
      meta: { requiresAuth: true },
    },
    {
      path: '/threads/:threadId/edit',
      name: 'ThreadEditView',
      component: ThreadEditView,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/books/:bookId/thread/create',
      name: 'ThreadCreateView',
      component: ThreadCreateView,
      props: true,  // bookId를 props로 넘기기
      meta: { requiresAuth: true },  // 인증이 필요한 라우트 => 쓰레드 작성은 로그인 필요
    },
    {
      path: '/profile/:userPk?',
      name: 'ProfileView',
      component: ProfileView,
      props: true,  // userId를 props로 넘기기
      meta: { requiresAuth: true },  // 인증이 필요한 라우트 => 프로필 조회는 로그인 필요
    },
    {
      path: '/profile/:userPk/edit',
      name: 'UserEditView',
      component: UserEditView,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/recommend',
      name: 'RecommendFormView',
      component: RecommendFormView, 
    },
    {
      path: '/recommend/result',
      name: 'RecommendView',
      component: RecommendView,
    },
  ],
})

export default router

router.beforeEach((to, from, next) => {
  const accountStore = useAccountStore()

  // 회원가입 라우트 진입 시 에러 초기화
  // if (to.name === 'SignUpView') {
  //   accountStore.signUpError = ''
  // }

  // 인증이 필요한 라우트에 meta: { requiresAuth: true } 옵션을 추가했다
  if (to.meta.requiresAuth && !accountStore.token) {
    alert('로그인이 필요합니다.')
    next({ name: 'LogInView' })
  } else {
    next()
  }
})
