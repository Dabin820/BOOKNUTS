<!-- views/SignUpForm.vue -->
<template>
  <div class="signup-container d-flex justify-content-center align-items-center">
    <div class="signup-box mb-5">
      <h3 class="text-center fw-bold mb-4">회원가입</h3>
      <!-- 에러 메시지 표시 -->
      <div v-if="accountStore.signUpError" class="alert alert-danger my-2">
        {{ accountStore.signUpError }}
      </div>
      <form @submit.prevent="onSignUp">
        <!-- 아이디 -->
         <div class="mb-3">
           <label for="username" class="form-label">닉네임<span class="text-danger">*</span></label><br>
           <input type="text" id="username" v-model.trim="username" class="form-control" placeholder="아이디를 입력해주세요"><br>
         </div>
  
         <!-- 비밀번호 -->
          <div class="mb-3">
            <label for="password1" class="form-label">비밀번호 <span class="text-danger">*</span></label><br>
            <input type="password" id="password1" v-model.trim="password1" class="form-control" placeholder="비밀번호를 입력해주세요"><br>          
          </div>

          <div class="mb-3">
            <label for="password2">비밀번호 확인 <span class="text-danger">*</span></label>
            <span v-if="passwordError" class="text-danger small m-2">{{ passwordError }}</span>
            <br>
            <input type="password" id="password2" v-model.trim="password2" class="form-control" placeholder="비밀번호를 다시 입력해주세요"><br>
          </div>
          
          <!-- email -->
          <div class="mb-3">
            <label for="email" class="form-label">이메일</label><br>
            <input type="email" id="email" v-model.trim="email" class="form-control" placeholder="이메일을 입력해주세요"><br>
          </div>
          
          <!-- 나이 -->
          <div class="mb-3">
            <label for="age">나이 <span class="text-danger">*</span></label><br>
            <input type="number" id="age" v-model.number="age" class="form-control"><br>
          </div>
          
          <!-- 연간 독서량 -->
          <div class="mb-3">
            <label for="annual">연간 독서량</label><br>
            <select v-model="annualReadingAmount" class="form-select">
            <option disabled value="">아래의 옵션을 선택해주세요</option>
            <option value="1">5권 미만</option>
            <option value="2">10권 미만</option>
            <option value="3">10권 이상</option>
          </select>
          </div>
        
          <!-- 관심 장르 -->
          <div class="mb-3 mt-4">
              <label class="form-label">좋아하는 장르 <span class="text-danger">*</span></label>
              <div class="border rounded p-3 genre-box">
                <div v-for="category in categoryStore.categories" :key="category.id" class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'genre-' + category.id"
                    :value="category.id"
                    v-model="interestedGenres"
                  />
                  <label class="form-check-label" :for="'genre-' + category.id">
                    {{ category.name }}
                  </label>
                </div>
              </div>
          </div>
      
        <!-- 프로필 이미지 -->
        <div class="mb-3">
          <label for="profileImg" class="form-label">프로필 이미지</label>
          <input type="file" id="profileImg" @change="onUploadFile" class="form-control" />
        </div>

        <!-- 버튼 -->
        <button type="submit" class="btn btn-warning w-100 text-white fw-bold">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'
  import { useCategoryStore } from '@/stores/categories'

  const route = useRoute()
  const accountStore = useAccountStore()
  const categoryStore = useCategoryStore()

  const username = ref('')
  const email = ref('')
  const password1 = ref('')
  const password2 = ref('')
  const age = ref(null)
  const annualReadingAmount = ref('')
  const interestedGenres = ref([])
  const profileImg = ref(null)

  const passwordError = computed(() => {
    if (!password1.value || !password2.value) return ''
    if (password1.value !== password2.value) return '비밀번호가 일치하지 않습니다. 다시 입력해 주세요.'
    return ''
  })

  const onUploadFile = (e) => {
    profileImg.value = e.target.files[0]
  }

  const onSignUp = function () {
    if (passwordError.value) {
      // 이미 computed에서 에러 메시지 생성됨
      password1.value = ''
      password2.value = ''
      return
    }
    const userInfo = {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
      age: age.value,
      annualReadingAmount: annualReadingAmount.value,
      interestedGenres: interestedGenres.value,
      profileImg: profileImg.value,
    }
    accountStore.signUp(userInfo)
  }

  onMounted(() => {
    accountStore.signUpError = ''
  })


</script>

