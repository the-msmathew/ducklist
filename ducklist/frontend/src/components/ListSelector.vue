<template>
  <div>
    <h2>Your Lists</h2>

    <ul>
      <li 
        v-for="l in lists" 
        :key="l.id"
        :class="{ selected: l.id === selectedListId }"
        @click="$emit('select', l.id)"
      >
        {{ l.title }}
      </li>
    </ul>

    <NewItemForm 
      placeholder="New list name..."
      @submit="title => $emit('createList', title)"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import NewItemForm from './NewItemForm.vue'

export default defineComponent({
  components: { NewItemForm },
  props: {
    lists: { type: Array, required: true },
    selectedListId: { type: Number, required: false }
  }
})
</script>

<style scoped>
.selected {
  font-weight: bold;
  color: blue;
}
</style>
