<!-- views/ProfileView.vue -->
<template>
  <div>
    <Profile :userPk="userPk" />
  </div>
</template>

<script setup>
  import { computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'
  import Profile from '@/components/Profile.vue'

  const route = useRoute()
  const router = useRouter()
  const accountStore = useAccountStore()

   // ✅ user와 token이 모두 유효한지 확인
  const isAuthenticated = computed(() => accountStore.user && accountStore.token)

  const userPk = computed(() => {
    return route.params.userPk || accountStore.user?.pk || null
  })

  const canAccess = computed(() => {
    return isAuthenticated.value && userPk.value
  })

  // ✅ 잘못된 접근일 경우 메인으로 리다이렉트
  if (!canAccess.value) {
    router.replace({ name: 'MainView' })
  }
</script>

<style scoped>

</style>