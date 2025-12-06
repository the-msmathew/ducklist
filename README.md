# DuckList 🦆 – To-Do List with Ducks

A simple FastAPI backend for managing to-do lists and tasks, with persistent storage via SQLModel (SQLite). Perfect for learning FastAPI, SQLModel, and building a full-stack app with a future UI.

---

## Features

- Create, read, update, and delete **Task Lists**  
- Create, read, update, and delete **Tasks** within lists  
- Persistent storage using **SQLite** and **SQLModel ORM**  
- Interactive API documentation via **Swagger UI**  
- Organized project structure with **routers** and **models**  

*Future ideas:*  
- User authentication (login/signup)  
- Optional task locations and due dates  
- Fun UI with ducks lining up when tasks are completed 🦆  

---

## Tech Stack

- **Backend:** Python, FastAPI  
- **Database/ORM:** SQLModel (SQLite)  
- **API Docs:** Swagger UI (built into FastAPI)  
- **Package Management:** Poetry  

---

## Project Structure


---

## Getting Started

Follow these steps to run DuckList locally:

### 1. Clone the repo

Backend

```bash
git clone https://github.com/the-msmathew/ducklist.git
cd ducklist
poetry install
poetry shell
uvicorn ducklist.app:app --reload
```

Frontend

```bash
npm create vite@latest ducklist-frontend
cd ducklist-frontend
npm install
npm run dev
```
Install nvm
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.6/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

```


API root: http://127.0.0.1:8000

Swagger UI (interactive API docs): http://127.0.0.1:8000/docs

---