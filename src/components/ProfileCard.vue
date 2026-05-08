<template>
  <div class="profile-card">
    <div class="pic-wrapper">
      <img v-if="picUrl" :src="picUrl" :alt="profile.name" class="profile-pic" />
      <div v-else class="profile-pic placeholder">{{ profile.name?.[0] }}</div>
    </div>

    <div class="profile-info">
      <h3>{{ profile.name }}<span v-if="profile.age">, {{ profile.age }}</span></h3>
      <p v-if="profile.location" class="location">📍 {{ profile.location }}</p>
      <p class="bio">{{ profile.bio || 'No bio provided.' }}</p>

      <div v-if="profile.hobbie1 || profile.hobbie2 || profile.hobbie3" class="hobbies">
        <span v-if="profile.hobbie1" class="tag">{{ profile.hobbie1 }}</span>
        <span v-if="profile.hobbie2" class="tag">{{ profile.hobbie2 }}</span>
        <span v-if="profile.hobbie3" class="tag">{{ profile.hobbie3 }}</span>
      </div>

      <div class="actions">
        <button class="btn-like" @click="$emit('like', profile.id)">❤️ Like</button>
        <button class="btn-pass" @click="$emit('pass', profile.id)">✕ Pass</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps(['profile']);
defineEmits(['like', 'pass']);

const picUrl = computed(() => {
  if (!props.profile.pic || props.profile.pic === 'default.png') return null;
  return 'http://localhost:5000/static/uploads/' + props.profile.pic;
});
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  overflow: hidden;
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
}
.profile-card:hover { transform: translateY(-4px); }

.pic-wrapper { width: 100%; height: 220px; overflow: hidden; }
.profile-pic { width: 100%; height: 100%; object-fit: cover; }
.placeholder {
  width: 100%; height: 100%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; font-size: 4rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}

.profile-info { padding: 16px; display: flex; flex-direction: column; gap: 8px; flex: 1; }

h3 { margin: 0; font-size: 1.1rem; color: #1f2937; }

.location { margin: 0; font-size: 0.85rem; color: #6b7280; }

.bio {
  margin: 0; font-size: 0.9rem; color: #4b5563;
  display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden;
}

.hobbies { display: flex; flex-wrap: wrap; gap: 6px; }
.tag {
  background: #ede9fe; color: #6366f1;
  padding: 3px 10px; border-radius: 20px; font-size: 0.8rem;
}

.actions { display: flex; gap: 10px; margin-top: auto; padding-top: 8px; }

.btn-like, .btn-pass {
  flex: 1; padding: 10px;
  border: none; border-radius: 10px;
  font-weight: 600; cursor: pointer; font-size: 0.9rem;
}
.btn-like { background: #6366f1; color: white; }
.btn-like:hover { background: #4f46e5; }
.btn-pass { background: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; }
.btn-pass:hover { background: #e5e7eb; }
</style>