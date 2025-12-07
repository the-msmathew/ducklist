<template>
    <div class="page-container">
      <h1 class="list-title">{{ listTitle }}</h1>
  
      <section class="add-task-section">
        <h2>Add Task</h2>
        <input v-model="newTaskTitle" placeholder="Task title" />
  
        <input type="date" v-model="newTaskDueDate" />
  
        <input type="text" v-model="newTaskLocation" placeholder="Location (optional)" />
  
        <button @click="addTask">Add Task</button>
      </section>
  
      <section class="tasks-section">
        <h2>Tasks</h2>
        <ul>
          <li v-for="task in tasks" :key="task.id" class="task-item">
            <input type="checkbox" v-model="task.completed" @change="toggleTask(task)" />
            <span :class="{ completed: task.completed }">{{ task.title }}</span>
            <span v-if="task.due_date"> - Due: {{ formatDate(task.due_date) }}</span>
            <span v-if="task.location"> ({{ task.location }})</span>
            <button @click="removeTask(task)">Delete</button>
          </li>
        </ul>
      </section>
  
      <!-- Ducks floating around -->
      <img
        v-for="duck in ducks"
        :key="duck.id"
        src="/duck.png"
        alt="Rubber Duck"
        class="duck"
        :style="{
          top: duck.y + 'px',
          left: duck.x + 'px',
          filter: 'hue-rotate(' + duck.hue + 'deg)'
        }"
      />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { getList, getTasks, createTask, updateTask, deleteTask } from '../api';
  import type { Task } from '../api';
  
  const route = useRoute();
  const listId = route.params.id as string;
  
  const listTitle = ref('');
  const tasks = ref<Task[]>([]);
  
  const newTaskTitle = ref('');
  const newTaskDueDate = ref('');
  const newTaskLocation = ref('');
  
  // Ducks with position, velocity, hue rotation, and taskId
  const ducks = ref<
    {
      id: number;
      x: number;
      y: number;
      vx: number;
      vy: number;
      taskId: number;
      hue: number; // For color variation with hue-rotate, no whites
    }[]
  >([]);
  
  // Create a duck for a task with random position and velocity
  function createDuckForTask(task: Task) {
    const speed = 1.5;
    ducks.value.push({
      id: Date.now() + Math.random(),
      x: Math.random() * (window.innerWidth - 50),
      y: Math.random() * (window.innerHeight - 150),
      vx: (Math.random() * 2 - 1) * speed,
      vy: (Math.random() * 2 - 1) * speed,
      taskId: task.id,
      hue: Math.random() * 360, // random hue for color variation, avoid white
    });
  }
  
  async function loadTasks() {
    const list = await getList(listId);
    listTitle.value = list.title;
  
    tasks.value = await getTasks(listId);
  
    ducks.value = [];
    tasks.value.forEach((task) => {
      createDuckForTask(task);
      if (task.completed) {
        // Immediately line up completed ducks at top row
        const duck = ducks.value.find((d) => d.taskId === task.id);
        if (duck) {
          duck.y = 10;
          const topDucks = ducks.value.filter((d) =>
            tasks.value.find((t) => t.id === d.taskId)?.completed
          );
          duck.x = topDucks.indexOf(duck) * 60 + 10;
          duck.vx = 0;
          duck.vy = 0;
        }
      }
    });
  }
  
  async function addTask() {
    if (!newTaskTitle.value.trim()) return;
  
    const task = await createTask(listId, {
      title: newTaskTitle.value,
      completed: false,
      due_date: newTaskDueDate.value || null,
      location: newTaskLocation.value || null,
    });
  
    tasks.value.push(task);
    createDuckForTask(task);
  
    newTaskTitle.value = '';
    newTaskDueDate.value = '';
    newTaskLocation.value = '';
  }
  
  async function toggleTask(task: Task) {
    await updateTask(listId, task.id, task);
  
    const duck = ducks.value.find((d) => d.taskId === task.id);
    if (duck) {
      if (task.completed) {
        // Snap to top row and stop moving
        duck.y = 10;
        const topDucks = ducks.value.filter((d) =>
          tasks.value.find((t) => t.id === d.taskId)?.completed
        );
        duck.x = topDucks.indexOf(duck) * 60 + 10;
        duck.vx = 0;
        duck.vy = 0;
      } else {
        // Random position and velocity again
        duck.y = Math.random() * (window.innerHeight - 150);
        duck.x = Math.random() * (window.innerWidth - 50);
        const speed = 1.5;
        duck.vx = (Math.random() * 2 - 1) * speed;
        duck.vy = (Math.random() * 2 - 1) * speed;
      }
    }
  }
  
  async function removeTask(task: Task) {
    await deleteTask(listId, task.id);
    tasks.value = tasks.value.filter((t) => t.id !== task.id);
    ducks.value = ducks.value.filter((d) => d.taskId !== task.id);
  }
  
  function formatDate(dateStr: string) {
    return new Date(dateStr).toLocaleDateString();
  }
  
  // Animate ducks by updating their position every frame
  function animateDucks() {
    ducks.value.forEach((duck) => {
      // Stop movement if velocity zero (top row)
      if (duck.vx === 0 && duck.vy === 0) return;
  
      duck.x += duck.vx;
      duck.y += duck.vy;
  
      // Bounce off edges
      if (duck.x < 0) {
        duck.x = 0;
        duck.vx = -duck.vx;
      } else if (duck.x > window.innerWidth - 40) {
        duck.x = window.innerWidth - 40;
        duck.vx = -duck.vx;
      }
  
      if (duck.y < 50) {
        duck.y = 50;
        duck.vy = -duck.vy;
      } else if (duck.y > window.innerHeight - 40) {
        duck.y = window.innerHeight - 40;
        duck.vy = -duck.vy;
      }
    });
  
    requestAnimationFrame(animateDucks);
  }
  
  onMounted(() => {
    loadTasks();
    animateDucks();
  });
  </script>
  
  <style scoped>
  .page-container {
    position: relative;
    min-height: 100vh;
    padding: 20px;
    background: linear-gradient(to top, #001f4d, #66b2ff); /* dark blue bottom, light blue top */
    overflow-x: hidden;
    overflow-y: auto;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
  }
  
  .list-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 25px;
    color: black; /* black title */
    user-select: none;
  }
  
  .add-task-section,
  .tasks-section {
    max-width: 600px;
    margin: 0 auto 30px auto;
    background: rgba(255, 255, 255, 0.15);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  }
  
  .add-task-section h2,
  .tasks-section h2 {
    margin-bottom: 15px;
  }
  
  .add-task-section input,
  .add-task-section button {
    margin: 6px 6px 12px 0;
    padding: 8px 12px;
    border-radius: 6px;
    border: none;
    font-size: 1rem;
  }
  
  .add-task-section button {
    background-color: #ffc107;
    color: #333;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.25s ease-in-out;
  }
  
  .add-task-section button:hover {
    background-color: #ffa000;
  }
  
  .tasks-section ul {
    list-style: none; /* remove bullet points */
    padding-left: 0;
  }
  
  .task-item {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
  }
  
  .task-item input[type='checkbox'] {
    width: 20px;
    height: 20px;
    cursor: pointer;
    margin: 0;
  }
  
  .task-item span {
    flex-grow: 1;
    font-size: 1.1rem;
    user-select: none;
  }
  
  .task-item span.completed {
    text-decoration: line-through;
    opacity: 0.6;
  }
  
  .task-item button {
    background: #ff5252;
    border: none;
    color: white;
    border-radius: 6px;
    padding: 5px 12px;
    cursor: pointer;
    transition: background-color 0.25s ease-in-out;
  }
  
  .task-item button:hover {
    background-color: #ff0000;
  }
  
  /* Duck image style */
  .duck {
    position: fixed;
    width: 40px;
    height: 40px;
    user-select: none;
    pointer-events: none;
    transition: filter 0.3s ease; /* smooth hue rotate */
    will-change: transform, top, left;
    z-index: 9999;
    image-rendering: pixelated;
  }
  </style>
  