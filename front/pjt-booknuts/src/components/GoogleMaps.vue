<!-- views/GoogleMaps.vue -->
<template>
  <div class="map-wrapper">
    <iframe :src="mapUrl"
      class="google-map"
      allowfullscreen
      loading="lazy"
      referrerpolicy="no-referrer-when-downgrade"
    ></iframe>
  </div>
</template>


<script setup>
  import { ref, onMounted } from 'vue'

  const lat = ref(null)
  const lng = ref(null)
  const error = ref('')
  const mapUrl = ref('')

  // 위치 정보 가져오기
  const getCurrentLocation = () => {
    navigator.geolocation.getCurrentPosition(
      pos => {
        lat.value = pos.coords.latitude
        lng.value = pos.coords.longitude
        error.value = ''
        updateMap()
      },
      err => {
        error.value = `위치 조회 실패: ${err.message}`
      }
    )
  }

  // iframe 지도 업데이트 (키워드 고정)
  const updateMap = () => {
    const fixedKeyword = '도서관 서점' // 키워드 고정
    mapUrl.value =
      `https://maps.google.com/maps` +
      `?q=${encodeURIComponent(fixedKeyword)}` + // 검색어 고정
      `&ll=${lat.value},${lng.value}` +
      `&z=14` +
      `&output=embed`
  }

  // 초기 위치 설정
  onMounted(() => {
    getCurrentLocation()
  })

</script>

<style scoped>
.map-wrapper {
  width: 100%;
  height: 400px;
  overflow: hidden;
  border-radius: 8px;
}

.google-map {
  width: 100%;
  height: 100%;
  border: none;
}
</style>