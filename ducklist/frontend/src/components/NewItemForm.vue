<template>
  <form @submit.prevent="submitForm">
    <input 
      v-model="text" 
      :placeholder="placeholder"
    />
    <button>Add</button>
  </form>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  props: {
    placeholder: { type: String, default: '' }
  },
  emits: ['submit'],
  setup(_, { emit }) {
    const text = ref('')

    const submitForm = () => {
      if (text.value.trim() === '') return
      emit('submit', text.value)
      text.value = ''
    }

    return { text, submitForm }
  }
})
</script>
