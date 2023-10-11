<!-- eslint-disable-next-line vue/no-unused-vars -->

<template>
  <div id="app">
    <header>
      <h1 style="color: black;">Task Management App</h1>
    </header>
    <main>
      <section class="sidebar">
        <h2>Categories</h2>
        <ul>
          <!-- eslint-disable-next-line vue/no-unused-vars -->
          <li v-for="(category, index) in categories" :key="index">
            <div class="category">
              <input v-model="category.name" />
              <button @click="deleteCategory(index)">Delete</button>
            </div>
          </li>
        </ul>
        <div class="add-category">
          <input v-model="newCategory" @keyup.enter="addCategory" placeholder="Add Category" />
        </div>
      </section>
      <section class="task-list">
        <div class="category-tasks" v-for="(category, index) in categories" :key="index">
          <h2>{{ category.name }} Tasks</h2>
          <vue-draggable-next v-model="category.tasks" @update="onTaskOrderChange">
            <ul>
              <li v-for="(task, taskIndex) in category.tasks" :key="task.id" :style="task.style">
                <div class="task-item">
                  <input type="checkbox" v-model="task.completed" @change="toggleTaskCompletion(category, task)" />
                  <label>{{ task.title }}</label>
                  <button class="delete-button" @click="deleteTask(category, taskIndex)">×</button>
                </div>
              </li>
            </ul>
        <div class="add-task">
          <input v-model="newTask[category.name]" @keyup.enter="addTask(category.name)" placeholder="Add Task" />
        </div>
      </vue-draggable-next>
    </div>
  </section>
  </main>
    <footer>
      <h3>INIAD@group16-team4</h3>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newCategory: '',
      categories: [],
      newTask: {},
    };
  },
  methods: {
    addCategory() {
      if (this.newCategory.trim() !== '') {
        this.categories.push({ name: this.newCategory, tasks: [] });
        this.newCategory = '';
      }
    },
    deleteCategory(index) {
      this.categories.splice(index, 1);
    },
    toggleTaskCompletion(task) {
      axios.put(`http://localhost:8000/api/tasks/${task.id}/`, { completed: !task.completed })
        .then(response => {
          task.completed = response.data.completed;
        })
        .catch(error => {
          console.error(error);
        });
    },
    onTaskOrderChange(newOrder) {
      this.tasks = newOrder;
    },
    addTask(categoryName) {
      const category = this.categories.find((cat) => cat.name === categoryName);
      if (category) {
        if (this.newTask[categoryName].trim() !== '') {
          category.tasks.push({
            title: this.newTask[categoryName],
            completed: false,
            style: {},
          });
          this.newTask[categoryName] = '';
        }
      }
    },
    deleteTask(category, taskIndex) {
      if (category && taskIndex >= 0 && taskIndex < category.tasks.length) {
        // カテゴリ内でタスクを削除
        category.tasks.splice(taskIndex, 1);
      }
    },
  },
};
</script>

<style scoped>
#app {
  font-family: 'Helvetica Neue', sans-serif;
  text-align: center;
  color: #333;
  padding: 20px;
  background-color: #8db4d6; /* くすみがかった水色 */
  min-height: 100vh; /* 画面全体に背景色を広げるため */
  display: flex;
  flex-direction: column;
}

header {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  color: black;
  text-align: left; /* テキストを左寄せにする */
}

.app-title {
  margin: 0;
  font-size: 24px;
}

main {
  flex-grow: 1; /* メインコンテンツを伸ばして画面いっぱいに広げる */
  display: flex;
  background-color: white;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #f0f0f0; /* サイドバーの背景色 */
  text-align: left; /* テキストを左寄せにする */
}

.sidebar h2 {
  margin-bottom: 10px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.sidebar button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.task-list {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto; /* タスクリストが大きくなった場合にスクロールできるようにする */
}

.task-list ul {
  list-style: none;
  padding: 0;
}

.task-item {
  display: inline-block;
  margin: 10px;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 5px;
  transition: transform 0.4s ease-in-out;
}

input[type="checkbox"] {
  margin-right: 10px;
  transform: scale(1.5);
  transition: transform 0.4s ease-in-out; /* アニメーションを追加 */
}

label {
  font-size: 18px;
  flex-grow: 1;
}

.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #ff0000; /* ボタンの色を赤に変更 */
  margin-left: 10px; /* ボタンの左側に余白を追加 */
}

footer {
  background-color: white;
  padding: 10px 0;
  text-align: center;
}

footer h3 {
  margin: 0;
  font-size: 18px;
}
</style>
