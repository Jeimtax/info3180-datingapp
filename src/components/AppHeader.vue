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

          <!-- Logout button (right side) -->
          <ul v-if="isLoggedIn" class="navbar-nav ms-auto">
            <li class="nav-item">
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

const router = useRouter();
const tokenRef = ref(localStorage.getItem('token'));

router.afterEach(() => {
  tokenRef.value = localStorage.getItem('token');
});

const isLoggedIn = computed(() => !!tokenRef.value);

function logout() {
  localStorage.removeItem('token');
  tokenRef.value = null;
  router.push('/login');
}
</script>

<style scoped>
.btn-link { background: none; border: none; padding: 0; cursor: pointer; }
</style>
