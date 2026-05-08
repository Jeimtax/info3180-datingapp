<template>
  <div class="explore-container">
    <h1>Browse Potential Matches</h1>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <input
        v-model="filters.search"
        type="text"
        placeholder="Search by name or bio..."
        class="filter-input filter-search"
      />

      <select v-model="filters.ageRange" class="filter-select">
        <option value="">All Ages</option>
        <option value="18-25">18 – 25</option>
        <option value="26-35">26 – 35</option>
        <option value="36-45">36 – 45</option>
        <option value="46-99">46+</option>
      </select>

      <input
        v-model="filters.location"
        type="text"
        placeholder="Filter by location..."
        class="filter-input filter-location"
      />

      <select v-model="filters.sort" class="filter-select">
        <option value="newest">Newest</option>
        <option value="oldest">Oldest</option>
      </select>
    </div>

    <!-- Interest filter (toggleable) -->
    <div class="interest-bar">
      <button class="btn-toggle" @click="showInterests = !showInterests">
        {{ showInterests ? 'Hide' : 'Show' }} Interest Filters
      </button>
      <button class="btn-reset" @click="resetFilters">Reset Filters</button>
    </div>

    <div v-if="showInterests" class="interest-input">
      <input
        v-model="filters.interest"
        type="text"
        placeholder="Filter by interest (e.g. hiking, gaming...)"
      />
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="state-msg">Loading profiles...</div>

    <!-- No results -->
    <div v-else-if="profiles.length === 0" class="state-msg empty">
      <p>No profiles match your filters. Try broadening your search.</p>
    </div>

    <!-- Results -->
    <div v-else class="profile-grid">
      <ProfileCard
        v-for="profile in profiles"
        :key="profile.id"
        :profile="profile"
        @like="handleAction('like', $event)"
        @pass="handleAction('pass', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import ProfileCard from '@/components/ProfileCard.vue';

const profiles = ref([]);
const isLoading = ref(false);
const showInterests = ref(false);

const filters = reactive({
  search: '',
  ageRange: '',
  location: '',
  interest: '',
  sort: 'newest'
});

let debounceTimer = null;

function buildUrl() {
  const params = new URLSearchParams();
  if (filters.search)   params.set('search',   filters.search);
  if (filters.location) params.set('location', filters.location);
  if (filters.interest) params.set('interest', filters.interest);
  if (filters.sort)     params.set('sort',     filters.sort);
  if (filters.ageRange) {
    const [min, max] = filters.ageRange.split('-');
    params.set('min_age', min);
    params.set('max_age', max);
  }
  const qs = params.toString();
  return `http://localhost:5000/api/v1/explore${qs ? '?' + qs : ''}`;
}

async function fetchProfiles() {
  const token = localStorage.getItem('token');
  if (!token) return;
  isLoading.value = true;
  try {
    const response = await fetch(buildUrl(), {
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' }
    });
    const data = await response.json();
    if (response.ok) profiles.value = data.profiles;
  } catch (error) {
    console.error('Error fetching profiles:', error);
  } finally {
    isLoading.value = false;
  }
}

async function handleAction(action, targetId) {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch('http://localhost:5000/api/v1/like', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ target_id: targetId, action })
    });
    const data = await response.json();
    if (action === 'like' && data.is_match) {
      alert("It's a Match! 🎉 Head to your Matches page to send a message.");
    }
  } catch (error) {
    console.error('Error:', error);
  } finally {
    profiles.value = profiles.value.filter(p => p.id !== targetId);
  }
}

function resetFilters() {
  filters.search = '';
  filters.ageRange = '';
  filters.location = '';
  filters.interest = '';
  filters.sort = 'newest';
}

watch(filters, () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(fetchProfiles, 350);
}, { immediate: true });
</script>

<style scoped>
.explore-container { padding: 24px; max-width: 1100px; margin: 0 auto; }
h1 { color: #6366f1; margin-bottom: 20px; }

.filter-bar {
  display: flex; flex-wrap: wrap; gap: 10px;
  margin-bottom: 10px;
}

.filter-input, .filter-select {
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
}
.filter-input:focus, .filter-select:focus {
  outline: none; border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}
.filter-search  { flex: 2; min-width: 180px; }
.filter-location { flex: 1; min-width: 140px; }
.filter-select  { min-width: 130px; }

.interest-bar {
  display: flex; gap: 10px; margin-bottom: 10px;
}

.btn-toggle {
  flex: 1; padding: 10px;
  background: #6366f1; color: white;
  border: none; border-radius: 8px;
  font-weight: 600; cursor: pointer;
}

.btn-reset {
  flex: 1; padding: 10px;
  background: #6b7280; color: white;
  border: none; border-radius: 8px;
  font-weight: 600; cursor: pointer;
}

.interest-input { margin-bottom: 14px; }
.interest-input input {
  width: 100%; padding: 10px 14px;
  border: 1px solid #d1d5db; border-radius: 8px;
  font-size: 0.95rem; box-sizing: border-box;
}
.interest-input input:focus {
  outline: none; border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.state-msg { text-align: center; color: #9ca3af; margin-top: 60px; font-size: 1rem; }
.empty p { margin: 0; }
</style>