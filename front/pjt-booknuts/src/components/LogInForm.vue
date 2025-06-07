<!-- views/SignUpForm.vue -->
<template>
  <div class="login-container d-flex justify-content-center align-items-center">
    <div class="login-box">
      <h3 class="text-center fw-bold mb-4">로그인</h3>
      <div v-if="accountStore.logInError" class="alert alert-danger my-2">
        {{ accountStore.logInError }}
      </div>  
      <form @submit.prevent="onLogIn">
        <div class="mb-3">
          <label for="username" class="form-label">닉네임 <span class="text-danger">*</span></label><br>
          <input type="text" id="username" v-model.trim="username" class="form-control"
          placeholder="아이디를 입력해주세요"><br>
        </div>
        
        <div>
          <label for="password" class="form-label">비밀번호</label><br>
          <input type="password" id="password" v-model.trim="password" class="form-control"
          placeholder="비밀번호를 입력해주세요"><br>
        </div>
  
        <button type="submit" value="Login" class="btn login-btn w-100">Login</button>
      </form>
    </div>
  </div>

</template>


<script setup>
  import { ref, onMounted } from 'vue'
  import { useAccountStore } from '@/stores/accounts'

  const accountStore = useAccountStore()

  const username = ref('')
  const password = ref('')

  onMounted(() => {
    accountStore.logInError = ''
  })

  const onLogIn = function () {
    const userInfo = {
      username: username.value, 
      password: password.value,
    }
    accountStore.logIn(userInfo)
  }

</script>



<style scoped>
  .login-btn {
    background-color: #ffc046;
    font-weight: bold;
    color: #fff;
    border: none;
  }
</style>