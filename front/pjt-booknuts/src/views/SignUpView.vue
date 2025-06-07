<!-- views/SignUpView.vue -->
<template>
  <div>
    <SignUpForm :key="route.fullPath" />
  </div>
</template>


<script setup>
  import { useRoute } from 'vue-router'
  import SignUpForm from '@/components/SignUpForm.vue'

  const route = useRoute()
</script>


<style scoped>

</style>