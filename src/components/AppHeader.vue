<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/">DriftDater</RouterLink>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <!-- Logged-in links -->
          <ul v-if="isLoggedIn" class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Dashboard</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/matches">Matches</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/messages">Messages</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/profile">Profile</RouterLink>
            </li>
          </ul>

          <!-- Guest links -->
          <ul v-else class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
          </ul>

          <!-- Right side: dark mode toggle + logout -->
          <ul class="navbar-nav ms-auto align-items-center">
            <li class="nav-item">
              <button class="dark-toggle" @click="toggleDark" :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'">
                {{ isDark ? '☀️' : '🌙' }}
              </button>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <button class="nav-link btn btn-link text-white" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useDarkMode } from '@/composables/useDarkMode.js';

const router = useRouter();
const { isDark, toggle: toggleDark } = useDarkMode();

const tokenRef = ref(localStorage.getItem('token'));
router.afterEach(() => { tokenRef.value = localStorage.getItem('token'); });
const isLoggedIn = computed(() => !!tokenRef.value);

function logout() {
  localStorage.removeItem('token');
  tokenRef.value = null;
  router.push('/login');
}
</script>

<style scoped>
.btn-link { background: none; border: none; padding: 0; cursor: pointer; }
.dark-toggle {
  background: none; border: none; font-size: 1.2rem;
  cursor: pointer; padding: 4px 8px; border-radius: 6px;
  transition: background 0.2s;
}
.dark-toggle:hover { background: rgba(255,255,255,0.15); }
</style>
