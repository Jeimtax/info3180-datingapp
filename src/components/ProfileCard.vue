<template>
  <div class="profile-card">
    <img :src="'http://localhost:5000/static/uploads/' + profile.pic" alt="Profile Picture" class="profile-pic" />
    <div class="profile-info">
      <h3>{{ profile.name }}</h3>
      <p class="bio">{{ profile.bio || "No bio provided." }}</p>
      <button @click="$emit('like', profile.id)" class="like-btn">❤️ Like</button>
    </div>
  </div>
</template>

<script setup>
defineProps(['profile']);
defineEmits(['like']);
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.2s;
}
.profile-card:hover { transform: translateY(-5px); }
.profile-pic { width: 100%; height: 250px; object-fit: cover; }
.profile-info { padding: 15px; text-align: center; }
.like-btn {
  background: #ff4d4d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}
</style>