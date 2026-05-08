<template>
  <div class="explore-container">
    <h1>Find Your Match</h1>
    <div v-if="profiles.length === 0" class="no-profiles">
      <p>No new profiles found. Check back later!</p>
    </div>
    <div class="profile-grid">
      <ProfileCard 
        v-for="profile in profiles" 
        :key="profile.id" 
        :profile="profile" 
        @like="handleLike"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ProfileCard from '@/components/ProfileCard.vue';

const profiles = ref([]);

// 1. Fetch profiles from your Flask /api/v1/explore route
async function fetchProfiles() {
  const token = localStorage.getItem('token'); // Get the JWT from login
  try {
    const response = await fetch("http://localhost:5000/api/v1/explore", {
      headers: {
        'Authorization': `Bearer ${token}` // Send the token to Flask!
      }
    });
    const data = await response.json();
    if (response.ok) {
      profiles.value = data.profiles;
    }
  } catch (error) {
    console.error("Error fetching profiles:", error);
  }
}

// 2. Handle the Like button
async function handleLike(targetId) {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch("http://localhost:5000/api/v1/like", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ target_id: targetId })
    });
    
    const data = await response.json();
    if (data.is_match) {
      alert("It's a Match! 🎉");
    }
    
    // Remove the liked profile from the screen
    profiles.value = profiles.value.filter(p => p.id !== targetId);
  } catch (error) {
    console.error("Error liking user:", error);
  }
}

onMounted(fetchProfiles);
</script>

<style scoped>
.explore-container { padding: 20px; max-width: 1000px; margin: 0 auto; }
.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.no-profiles { text-align: center; margin-top: 50px; color: #666; }
</style>