<template>
    <div>
      <h1>Tasks for List: {{ listTitle }}</h1>
  
      <section>
        <h2>Add Task</h2>
        <input v-model="newTaskTitle" placeholder="New task title" />
        <button @click="addTask">Add Task</button>
      </section>
  
      <section>
        <h2>Tasks</h2>
        <div v-if="tasks.length === 0">No tasks yet.</div>
        <ul>
          <li v-for="task in tasks" :key="task.id">
            {{ task.title }} - {{ task.completed ? '✅' : '❌' }}
          </li>
        </ul>
      </section>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  
  interface Task {
    id: number
    title: string
    completed: boolean
  }
  
  const route = useRoute()
  const listId = route.params.id as string
  const listTitle = ref('')
  const tasks = ref<Task[]>([])
  const newTaskTitle = ref('')
  
  async function loadTasks() {
    // Fetch list details
    const listRes = await axios.get(`http://localhost:8000/lists/${listId}`)
    listTitle.value = listRes.data.title
  
    // Fetch tasks for this list
    const tasksRes = await axios.get(`http://localhost:8000/lists/${listId}/tasks`)
    tasks.value = tasksRes.data
  }
  
  async function addTask() {
    if (!newTaskTitle.value.trim()) return
    const res = await axios.post(`http://localhost:8000/lists/${listId}/tasks`, {
      title: newTaskTitle.value,
    })
    tasks.value.push(res.data)
    newTaskTitle.value = ''
  }
  
  onMounted(loadTasks)
  </script>
  