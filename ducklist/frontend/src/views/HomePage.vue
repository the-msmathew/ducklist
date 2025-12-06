<template>
    <div>
      <h1>DuckList</h1>
  
      <section>
        <h2>Create List</h2>
        <input v-model="newListTitle" placeholder="New list title" />
        <button @click="addList">Add</button>
      </section>
  
      <section>
        <h2>Your Lists</h2>
        <div v-if="lists.length === 0">No lists yet.</div>
  
        <ul>
          <li v-for="list in lists" :key="list.id">
            <!-- Clickable link to ListPage -->
            <router-link :to="`/lists/${list.id}`">{{ list.title }}</router-link>
            <button @click="removeList(list.id)">Delete</button>
          </li>
        </ul>
      </section>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { getLists, createList, deleteList } from '../api'
  
  interface TaskList {
    id: number
    title: string
  }
  
  const lists = ref<TaskList[]>([])
  const newListTitle = ref('')
  
  async function loadLists() {
    lists.value = await getLists()
  }
  
  async function addList() {
    if (!newListTitle.value.trim()) return
    const created = await createList(newListTitle.value)
    lists.value.push(created)
    newListTitle.value = ''
  }
  
  async function removeList(id: number) {
    await deleteList(id)
    lists.value = lists.value.filter(l => l.id !== id)
  }
  
  onMounted(loadLists)
  </script>
  