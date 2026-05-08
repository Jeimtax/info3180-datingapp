<template>
  <div class="matches-container">
    <h1>Your Matches</h1>

    <div v-if="isLoading" class="state-msg">Loading your matches...</div>

    <div v-else-if="matches.length === 0" class="state-msg empty">
      <p>No mutual matches yet. Keep exploring!</p>
      <router-link to="/explore" class="btn-explore">Browse Profiles</router-link>
    </div>

    <div v-else class="matches-list">
      <div v-for="match in matches" :key="match.id" class="match-card">
        <div v-if="picUrl(match)" class="pic-wrapper">
          <img :src="picUrl(match)" :alt="match.name" class="match-pic" />
        </div>
        <div v-else class="match-pic placeholder-pic">
          {{ match.name?.[0] }}
        </div>

        <div class="match-info">
          <h2>{{ match.name }}</h2>
          <p class="bio">{{ match.bio || 'No bio yet.' }}</p>
        </div>

        <router-link :to="`/messages/${match.id}`" class="btn-message">
          Message
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const matches = ref([]);
const isLoading = ref(true);

function picUrl(match) {
  if (!match.pic || match.pic === 'default.png') return null;
  return 'http://localhost:5000/static/uploads/' + match.pic;
}

async function fetchMatches() {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch("http://localhost:5000/api/v1/matches", {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    if (response.ok) {
      matches.value = data.matches;
    }
  } catch (error) {
    console.error("Error fetching matches:", error);
  } finally {
    isLoading.value = false;
  }
}

onMounted(fetchMatches);
</script>

<style scoped>
.matches-container { max-width: 800px; margin: 40px auto; padding: 20px; }

h1 { color: #6366f1; margin-bottom: 24px; }

.state-msg { text-align: center; color: #888; margin-top: 60px; font-size: 1.1rem; }
.empty { display: flex; flex-direction: column; align-items: center; gap: 16px; }

.btn-explore {
  padding: 10px 28px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; border-radius: 8px; text-decoration: none;
  font-weight: 600;
}

.matches-list { display: flex; flex-direction: column; gap: 16px; }

.match-card {
  display: flex; align-items: center; gap: 16px;
  background: white; padding: 16px 20px;
  border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

.match-pic {
  width: 70px; height: 70px; border-radius: 50%;
  object-fit: cover; border: 3px solid #6366f1; flex-shrink: 0;
}

.placeholder-pic {
  width: 70px; height: 70px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; font-size: 1.8rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}

.match-info { flex: 1; min-width: 0; }
.match-info h2 { margin: 0 0 4px; font-size: 1.1rem; color: #1f2937; }
.bio { margin: 0; color: #6b7280; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.btn-message {
  padding: 10px 22px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; border-radius: 8px;
  text-decoration: none; font-weight: 600;
  white-space: nowrap; flex-shrink: 0;
}
</style>
