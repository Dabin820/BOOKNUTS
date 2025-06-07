<template>
  <div class="signup-container d-flex justify-content-center align-items-center">
    <div class="signup-box mb-5">
      <h3 class="text-center fw-bold mb-4">회원 정보 수정</h3>
      <form @submit.prevent="onSubmit">
        <!-- 이메일 -->
        <div class="mb-3">
          <label for="email" class="form-label">이메일</label>
          <input type="email" id="email" v-model="email" class="form-control" disabled />
        </div>

        <!-- 닉네임 -->
        <div class="mb-3">
          <label for="username" class="form-label">닉네임</label>
          <input type="text" id="username" v-model="username" class="form-control" disabled />
        </div>

        <!-- 나이 -->
        <div class="mb-3">
          <label for="age" class="form-label">나이</label>
          <input type="number" id="age" v-model.number="age" class="form-control" min="0" />
        </div>

        <!-- 연간 독서량 -->
        <div class="mb-3">
          <label for="annualReadingAmount" class="form-label">연간 독서량</label>
          <input type="number" id="annualReadingAmount" v-model.number="annualReadingAmount" class="form-control" min="0" />
        </div>

        <!-- 관심 장르 -->
        <div class="mb-3 mt-4">
          <label class="form-label">좋아하는 장르</label>
          <div v-if="categoryStore.categories && categoryStore.categories.length > 0" class="border rounded p-3 genre-box">
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
          <div v-else>카테고리 로딩 중...</div>
        </div>

        <!-- 프로필 이미지 -->
        <div class="mb-3">
          <label for="profileImg" class="form-label">프로필 이미지</label>
          <input type="file" id="profileImg" @change="onUploadFile" class="form-control" />
          <img v-if="profileImgUrl" :src="profileStore.getImgUrl(profileImgUrl)" class="mt-2" style="width:60px;" />
        </div>

        <!-- 버튼 -->
        <div class="d-flex gap-3">
          <button type="submit" class="btn btn-warning text-white fw-bold">정보수정</button>
          <button type="button" class="btn btn-outline-secondary" @click="$emit('close')">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { useAccountStore } from '@/stores/accounts'
  import { useCategoryStore } from '@/stores/categories'
  import { useProfileStore } from '@/stores/profiles'

  const props = defineProps({
    user: Object,
    isEdit: Boolean
  })
  const emit = defineEmits(['edit-done', 'close'])
  const categoryStore = useCategoryStore()
  const profileStore = useProfileStore()

  const accountStore = useAccountStore()
  const username = ref(props.user?.username || '')
  const email = ref(props.user?.email || '')
  const age = ref(props.user?.age || null)
  const annualReadingAmount = ref(props.user?.annual_reading_amount || '')
  const interestedGenres = ref(
    (props.user?.interested_genres_ids || []).map(Number)
  )
  const profileImg = ref(null)
  const profileImgUrl = ref(props.user?.profile_img || '')

  watch(() => props.user, (newUser) => {
    if (newUser) {
      username.value = newUser.username
      email.value = newUser.email
      age.value = newUser.age
      annualReadingAmount.value = newUser.annual_reading_amount
      interestedGenres.value = (newUser.interested_genres_ids || []).map(Number)
    }
  })

  const onUploadFile = (e) => {
    profileImg.value = e.target.files[0]
    if (profileImg.value) {
      profileImgUrl.value = URL.createObjectURL(profileImg.value)
    }
  }

  const onSubmit = async () => {
    const userInfo = {
      userId: accountStore.user?.id,
      age: age.value,
      annual_reading_amount: annualReadingAmount.value,
      interested_genres_ids: interestedGenres.value,
      profile_img: profileImg.value,
    }
    try {
      await accountStore.updateProfile(userInfo)
      alert('회원정보가 수정되었습니다.')
      emit('edit-done')
    } catch (err) {
      alert('회원정보 수정 실패: ' + (err.response?.data?.detail || err.message))
    }
  }
</script>


<style scoped>
</style>
