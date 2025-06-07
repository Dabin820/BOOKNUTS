<!-- App.vue -->
<template>
  <header>
    <nav class="navbar navbar-expand-lg bg-white py-3 shadow-sm">
      <div class="container">
        <!-- 왼쪽: 로고 -->
        <RouterLink :to="{name: 'MainView'}">
          <img :src="logoImage" alt="logo" class="logo-img me-2">
        </RouterLink>

      <!-- 오른쪽: 링크들 -->
       <div class="d-flex align-items-center ms-auto gap-4">
         <RouterLink :to="{name: 'MainView'}" class="nav-link" active-class="router-link-active">Home</RouterLink>
         <RouterLink :to="{name: 'BookListView'}" class="nav-link" active-class="router-link-active">Book</RouterLink> 
         <RouterLink :to="{name: 'ThreadListView'}" class="nav-link" active-class="router-link-active">Thread</RouterLink>
         
         <div v-if="!accountStore.isLogin" class="d-flex align-items-center gap-2">
           <RouterLink :to="{name: 'SignUpView'}" class="nav-link" active-class="router-link-active">회원가입</RouterLink>
           <RouterLink :to="{name: 'LogInView'}" class="btn btn-warning text-white fw-bold px-3" >로그인</RouterLink>
         </div>
         
         <div v-if="accountStore.isLogin" class="d-flex align-items-center gap-2">
          <RouterLink :to="{name: 'ProfileView', params:{userPk:accountStore.user?.id}}" class="nav-link" active-class="router-link-active">Profile</RouterLink>
          <form @submit.prevent="onLogOut" class="mb-0">
            <input type="submit" value="로그아웃" class="btn btn-outline-secondary px-3">
          </form>
        </div>
       
      </div>
      </div>
    </nav>
  </header>

  <!-- <RouterView :key="$route.fullPath" /> -->
  <RouterView />

  <footer class="text-center py-4">
    <img :src="logoImage" alt="logo" class="footer-logo">
  </footer>
</template>


<script setup>
  import { RouterLink, RouterView } from 'vue-router';
  import { useAccountStore  } from '@/stores/accounts'
  import logoImage from '@/assets/Image/logo.png'

  const accountStore = useAccountStore()
  
  const onLogOut = function () {
    accountStore.logOut()
  }


</script>

