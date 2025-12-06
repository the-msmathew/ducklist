const API_URL = "http://127.0.0.1:8000";

export async function getLists() {
  const res = await fetch(`${API_URL}/lists/`);
  return res.json();
}

export async function createList(title: string) {
  const res = await fetch(`${API_URL}/lists/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  return res.json();
}

export async function deleteList(id: number) {
  await fetch(`${API_URL}/lists/${id}`, {
    method: "DELETE",
  });
}

export async function updateList(id: number, title: string) {
  const res = await fetch(`${API_URL}/lists/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  return res.json();
}
