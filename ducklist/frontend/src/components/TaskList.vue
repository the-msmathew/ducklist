<template>
  <div>
    <h2>Tasks</h2>

    <ul>
      <li v-for="t in tasks" :key="t.id">
        {{ t.title }}
      </li>
    </ul>

    <NewItemForm 
      placeholder="New task..."
      @submit="createTask"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue'
import NewItemForm from './NewItemForm.vue'

interface Task {
  id: number
  title: string
}

export default defineComponent({
  components: { NewItemForm },
  props: {
    listId: { type: Number, required: true }
  },
  setup(props) {
    const tasks = ref<Task[]>([])

    const fetchTasks = async () => {
      const res = await fetch(`http://127.0.0.1:8000/lists/${props.listId}/tasks`)
      tasks.value = await res.json()
    }

    const createTask = async (title: string) => {
      const res = await fetch(`http://127.0.0.1:8000/lists/${props.listId}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      })
      const newTask = await res.json()
      tasks.value.push(newTask)
    }

    onMounted(fetchTasks)
    watch(() => props.listId, fetchTasks)

    return { tasks, createTask }
  }
})
</script>
