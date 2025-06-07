// stores/threads.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCategoryStore = defineStore('category', () => {

  const API_URL = 'http://127.0.0.1:8000/booknuts'
  // 임시
  const categories = ref([
    {id:1, name:'소설/시/희곡'},
    {id:2, name:'경제/경영'},
    {id:3, name:'자기계발'},
    {id:4, name:'인문/교양'},
    {id:5, name:'취미/실용'},
    {id:6, name:'어린이/청소년'},
    {id:7, name:'과학'},
  ])

  const getCategories = () => {
    axios({
      method: 'get',
      url: `${API_URL}/categories/`
    })
      .then(res => {
        categories.value = res.data
      })
      .catch(err => {
        console.error(err)
      })
  }

  return {
    categories,
    getCategories,
  }
})