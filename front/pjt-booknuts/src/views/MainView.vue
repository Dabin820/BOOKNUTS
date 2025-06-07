<!-- views/MainView.vue -->
<template>
  <header class="header-wrapper">
    <section>
      <div class="container header-inner py-5">
        <div class="row align-items-center text-center text-md-start">
          <!-- 토리이미지 -->
          <div class="col-md-5 mb-4 mb-md-0 d-flex justify-content-center">
              <div class="circle-bg">
                <img :src="toriImage" alt="Main Tori" class="main-tori" />
              </div>
            </div>
          <!-- 소개 페이지 -->
          <div class="col-md-7">
            <h1 class="fw-bold mb-3">도서 디깅 클럽: BOOKNUTS</h1>
            <h5 class="mb-3">책을 몰라도 책을 좋아 할 수 있죠</h5>
            <p class="text-muted">자주는 아니지만 가끔은 책을 읽고 싶은 당신을 위해 AI 다람쥐 토리가 맞춤형 책을 추천해드립니다</p>
          </div>
        </div>
      </div>
    </section>
  </header>
  <main class="p-0 m-0">
    <!-- 토리 추천 -->
    <section class="p-0 m-0 ">
      <div class="container p-0 ">
        <AIRecommendations />
      </div>
    </section>

    <!-- 베스트셀러 -->
    <section>
      <Bestseller />
    </section>

    <!-- popular threads -->
    <section>
      <PopularThreads />
    </section>

  </main>

</template>


<script setup>
  import {onMounted} from 'vue'
  import {useBookStore} from '@/stores/books'
  import {useThreadStore} from '@/stores/threads'
  import AIRecommendations from '@/components/AIRecommendations.vue'
  import Bestseller from '@/components/Bestsellers.vue'
  import PopularThreads from '@/components/PopularThreads.vue'
  import toriImage from '@/assets/Image/maintori.png'
  import '@/assets/styles/global.css'

  const threadStore = useThreadStore()
  const bookStore = useBookStore()

  onMounted(() =>{
    bookStore.getBooks()
    threadStore.getThreads()
  })
</script>

<!-- <style scoped>

</style> -->