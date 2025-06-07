<template>
  <div>
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="error">에러: {{ error }}</div>
    <div v-else>
      <UserEditForm 
        :user="profile" 
        :isEdit="true" 
        @edit-done="onEditDone" @close="onCancel" 
      />
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'
  import { useProfileStore } from '@/stores/profiles'
  import UserEditForm from '@/components/UserEditForm.vue'

  const route = useRoute()
  const router = useRouter()
  const profileStore = useProfileStore()
  const accountStore = useAccountStore()

  const profile = ref(null)
  const loading = ref(true)
  const error = ref(null)

  const fetchProfile = async () => {
    loading.value = true
    error.value = null
    try {
      profile.value = await profileStore.getProfile(route.params.userPk)
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  onMounted(fetchProfile)

  const onCancel = () => {
    // 프로필 페이지로 이동 등 원하는 동작
    alert('회원 정보 수정을 취소합니다.')
    router.push({ name: 'ProfileView', params: { userPk: route.params.userPk } }).catch(() => {})
  }

  // 수정 완료 시 프로필 페이지로 이동
  const onEditDone = async () => {
    // 회원정보 수정 후, 내 프로필 다시 불러오기 (store.user도 갱신되었겠지만, 안전하게 fetch)
    await profileStore.getProfile(route.params.userPk)
    // alert('회원 정보가 수정되었습니다.')
    router.push({ name: 'ProfileView', params: { userPk: route.params.userPk } }).catch(() => {})
  }
</script>


<style scoped>
</style>


