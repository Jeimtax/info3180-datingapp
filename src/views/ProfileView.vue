<template>
  <div class="profile-container">
    <div v-if="user" class="profile-header">
      <img :src="'http://localhost:5000/static/uploads/' + user.pic" alt="My Photo" class="main-pic" />
      <h1>{{ user.first_name }} {{ user.last_name }}</h1>
      <p class="username">@{{ user.username }}</p>
    </div>

    <div v-if="user" class="profile-details">
      <div class="detail-card">
        <h3>About Me</h3>
        <p>{{ user.bio || "Write something interesting about yourself!" }}</p>
      </div>

      <div class="detail-card">
        <h3>Contact Info</h3>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Location:</strong> {{ user.location }}</p>
      </div>
    </div>

    <div v-else class="loading">
      <p>Loading your profile...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const user = ref(null);

async function fetchMyProfile() {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch("http://localhost:5000/api/v1/profile", {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await response.json();
    if (response.ok) {
      user.value = data;
    } else {
      console.error("Failed to load profile");
    }
  } catch (error) {
    console.error("Network error:", error);
  }
}

onMounted(fetchMyProfile);
</script>

<style scoped>
.profile-container { max-width: 800px; margin: 40px auto; padding: 20px; }
.profile-header { text-align: center; margin-bottom: 30px; }
.main-pic { width: 180px; height: 180px; border-radius: 50%; object-fit: cover; border: 5px solid #42b983; }
.username { color: #666; font-style: italic; }
.profile-details { display: grid; gap: 20px; }
.detail-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
h3 { color: #42b983; margin-top: 0; }
</style>