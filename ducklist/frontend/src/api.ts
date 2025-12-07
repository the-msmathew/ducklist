// src/api.ts
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export interface Task {
  id: number;
  title: string;
  completed: boolean;
  due_date: string | null;
  location?: string | null;
}

// --- Lists ---
export async function getLists() {
  const res = await axios.get(`${API_URL}/lists/`);
  return res.data;
}

export async function createList(title: string) {
  const res = await axios.post(`${API_URL}/lists/`, { title });
  return res.data;
}

export async function deleteList(id: number) {
  await axios.delete(`${API_URL}/lists/${id}`);
}

export async function updateList(id: number, title: string) {
  const res = await axios.put(`${API_URL}/lists/${id}`, { title });
  return res.data;
}

export async function getList(id: number) {
  const res = await axios.get(`${API_URL}/lists/${id}`);
  return res.data;
}

// --- Tasks ---
export async function getTasks(listId: string | number) {
  const res = await axios.get(`${API_URL}/lists/${listId}/tasks`);
  return res.data;
}

export async function createTask(listId: string | number, task: Partial<Task>) {
  const res = await axios.post(`${API_URL}/lists/${listId}/tasks`, task);
  return res.data;
}

export async function updateTask(listId: string | number, taskId: number, task: Partial<Task>) {
  const res = await axios.put(`${API_URL}/lists/${listId}/tasks/${taskId}`, task);
  return res.data;
}

export async function deleteTask(listId: string | number, taskId: number) {
  await axios.delete(`${API_URL}/lists/${listId}/tasks/${taskId}`);
}
