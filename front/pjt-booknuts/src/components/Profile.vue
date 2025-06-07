<!-- views/Profile.vue -->
<template>
  <div class="container py-5">
    <!-- 상단: 제목 + 프로필 이미지 -->
    <div class="row align-items-center mb-4">
      <!-- 좌측: 제목 -->
      <div class="col-md-6">
        <h3 class="fw-bold mb-3">{{ profile?.username }}님의 Profile </h3>
      </div>

      <!-- 우측: 프로필 이미지만 -->
      <div class="col-md-6 text-end">
        <img
          :src="profileStore.getImgUrl(profile?.profile_img)"
          alt="프로필 이미지"
          class="img-fluid rounded shadow-sm"
          style="max-width: 160px"
          v-if="profile?.profile_img"
        />
      </div>
    </div>

    <!-- 프로필 카드 -->
    <div class="card p-4 mb-4 shadow-sm">
      <h5 class="fw-bold mb-3">{{ profile?.username }} 님의 정보</h5>
      <ul class="list-unstyled mb-0">
        <li><strong>📧 이메일:</strong> {{ profile?.email }}</li>
        <li><strong>🎂 나이:</strong> {{ profile?.age }}</li>
        <li><strong>📚 연간 독서량:</strong> {{ profile?.annual_reading_amount }}</li>
        <li><strong>🎯 관심 장르:</strong> {{ profile?.interested_genres?.join(', ') || '없음' }}</li>
      </ul>
    </div>

    <hr class="mt-5">

    <!-- 유저 서재 -->
    <UserLibraryList :userPk="props.userPk" />

    <hr>

    <!-- 유저가 작성한 쓰레드 -->
    <UserThreadList :userPk="props.userPk" />

    <hr>

    <!-- 회원 관리 버튼 -->
    <div v-if="isMine" class="d-flex justify-content-between">
      <button class="btn btn-warning" @click="goToEdit">회원 정보 수정</button>
      <button class="btn btn-outline-secondary" @click="onDeleteAccount">회원 탈퇴</button>
    </div>
  </div>
</template>



<script setup>
  import { ref, onMounted, watch, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'
  import { useProfileStore } from '@/stores/profiles'
  import UserLibraryList from './UserLibraryList.vue'
  import UserThreadList from './UserThreadList.vue'

  const router = useRouter()
  const props = defineProps({
    userPk: {
      type: [Number, String],
      required: false 
    }
  })
  const accountStore = useAccountStore()
  const profileStore = useProfileStore()

  const isMine = computed(() => {
    // accountStore.user?.pk와 props.userPk를 문자열로 비교 (타입 불일치 방지)
    return Number(accountStore.user?.pk) === Number(props.userPk)
  })

  // 프로필 정보
  const profile = ref(null)
  const loading = ref(true)
  const error = ref(null)

  const fetchProfile = async () => {
  loading.value = true
  error.value = null
    try {
      profile.value = await profileStore.getProfile(props.userPk)
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
     if (!props.userPk) {
    router.replace({ name: 'MainView' })
    return
  }
    fetchProfile()
    // fetchUserThreads()
  })

  watch(() => props.userPk, () => {
     if (!props.userPk) {
    router.replace({ name: 'MainView' })
    return
  }
    fetchProfile()
    // fetchUserThreads()
  })

  

  // 회원 정보 수정
  const goToEdit = () => {
    router.push({ name: 'UserEditView', params: { userPk: props.userPk } })
  }

  // 회원 탈퇴
  const onDeleteAccount = async () => {
    if (!confirm('정말로 탈퇴하시겠습니까?\n탈퇴 후에는 복구할 수 없습니다.')) return
    try {
      await accountStore.deleteAccount(props.userPk)
      alert('탈퇴가 완료되었습니다.\n그동안 이용해주셔서 감사합니다.')
      router.push({ name: 'MainView' })
    } catch (err) {
      alert('회원 탈퇴 중 오류가 발생했습니다: ' + (err.response?.data?.detail || err.message))
    }
  }

</script>

<style scoped>

</style>