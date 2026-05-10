<template>
  <div class="favs-container">
    <h1>Bookmarked Profiles</h1>

    <div v-if="isLoading" class="state-msg">Loading bookmarks...</div>

    <div v-else-if="favorites.length === 0" class="state-msg empty">
      <p>No bookmarks yet. Star a profile on the Explore page to save it here.</p>
      <router-link to="/explore" class="btn-explore">Browse Profiles</router-link>
    </div>

    <div v-else class="favs-list">
      <div v-for="fav in favorites" :key="fav.id" class="fav-card">
        <img v-if="picUrl(fav) && !failedPics.has(fav.id)" :src="picUrl(fav)" :alt="fav.name" class="fav-pic" @error="failedPics.add(fav.id)" />
        <div v-else class="fav-pic placeholder-pic">{{ fav.name?.[0] }}</div>

        <div class="fav-info">
          <h2>{{ fav.name }}</h2>
          <p class="bio">{{ fav.bio || 'No bio yet.' }}</p>
        </div>

        <button class="btn-remove" @click="removeFavorite(fav.id)" title="Remove bookmark">★</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const favorites = ref([])
const isLoading = ref(true)
const failedPics = reactive(new Set())

function picUrl(fav) {
  if (!fav.pic || fav.pic === 'default.png') return null
  return 'http://localhost:5000/static/uploads/' + fav.pic
}

async function fetchFavorites() {
  const token = localStorage.getItem('token')
  try {
    const res = await fetch('http://localhost:5000/api/v1/favorites', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) favorites.value = data.favorites
  } catch (e) {
    console.error('Error loading favorites:', e)
  } finally {
    isLoading.value = false
  }
}

async function removeFavorite(targetId) {
  const token = localStorage.getItem('token')
  try {
    const res = await fetch('http://localhost:5000/api/v1/favorites', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_id: targetId })
    })
    if (res.ok) {
      favorites.value = favorites.value.filter((f) => f.id !== targetId)
    }
  } catch (e) {
    console.error('Error removing favorite:', e)
  }
}

onMounted(fetchFavorites)
</script>

<style scoped>
.favs-container { max-width: 800px; margin: 40px auto; padding: 20px; }

h1 { color: #6366f1; margin-bottom: 24px; }

.state-msg { text-align: center; color: #888; margin-top: 60px; font-size: 1.1rem; }
.empty { display: flex; flex-direction: column; align-items: center; gap: 16px; }

.btn-explore {
  padding: 10px 28px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; border-radius: 8px; text-decoration: none; font-weight: 600;
}

.favs-list { display: flex; flex-direction: column; gap: 16px; }

.fav-card {
  display: flex; align-items: center; gap: 16px;
  background: white; padding: 16px 20px;
  border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

.fav-pic {
  width: 70px; height: 70px; border-radius: 50%;
  object-fit: cover; border: 3px solid #f59e0b; flex-shrink: 0;
}

.placeholder-pic {
  width: 70px; height: 70px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; font-size: 1.8rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}

.fav-info { flex: 1; min-width: 0; }
.fav-info h2 { margin: 0 0 4px; font-size: 1.1rem; color: #1f2937; }
.bio {
  margin: 0; color: #6b7280; font-size: 0.9rem;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.btn-remove {
  background: none; border: none;
  font-size: 1.4rem; color: #f59e0b;
  cursor: pointer; flex-shrink: 0;
  padding: 6px; border-radius: 50%;
  transition: background 0.15s;
}
.btn-remove:hover { background: #fef3c7; }
</style>