<template>
  <div class="profile-container">
    <template v-if="user && !isEditing">
      <div class="profile-header">
        <div v-if="picUrl" class="pic-wrapper">
          <img :src="picUrl" alt="Profile Photo" class="main-pic" />
        </div>
        <div v-else class="main-pic placeholder-pic">
          {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
        </div>
        <h1>{{ user.first_name }} {{ user.last_name }}</h1>
        <p class="username">@{{ user.username }}</p>
        <p class="tagline">{{ user.relationship_goal }} · {{ user.location }}</p>
        <button class="btn-edit" @click="startEdit">Edit Profile</button>
      </div>

      <div class="profile-details">
        <div class="detail-card">
          <h3>About Me</h3>
          <p>{{ user.bio || "Write something interesting about yourself!" }}</p>
          <p><strong>Age:</strong> {{ user.age || '—' }}</p>
          <p><strong>Gender:</strong> {{ user.gender || '—' }}</p>
        </div>

        <div class="detail-card">
          <h3>Interests</h3>
          <div class="hobbies">
            <span v-if="user.hobbie1" class="tag">{{ user.hobbie1 }}</span>
            <span v-if="user.hobbie2" class="tag">{{ user.hobbie2 }}</span>
            <span v-if="user.hobbie3" class="tag">{{ user.hobbie3 }}</span>
            <span v-if="!user.hobbie1 && !user.hobbie2 && !user.hobbie3" class="no-data">No interests added yet</span>
          </div>
        </div>

        <div class="detail-card">
          <h3>Contact Info</h3>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Location:</strong> {{ user.location || '—' }}</p>
          <p><strong>Visibility:</strong> {{ user.visibility }}</p>
        </div>
      </div>
    </template>

    <template v-if="isEditing">
      <div class="edit-card">
        <h2>Edit Profile</h2>

        <div v-if="saveError" class="alert alert-danger">{{ saveError }}</div>
        <div v-if="saveSuccess" class="alert alert-success">{{ saveSuccess }}</div>

        <form @submit.prevent="saveProfile">
          <div class="form-row">
            <div class="form-group">
              <label>First Name</label>
              <input v-model="editData.first_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Last Name</label>
              <input v-model="editData.last_name" type="text" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Age</label>
              <input v-model="editData.age" type="number" min="18" max="99" />
            </div>
            <div class="form-group">
              <label>Gender</label>
              <select v-model="editData.gender">
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Non-binary">Non-binary</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Location</label>
            <input v-model="editData.location" type="text" />
          </div>

          <div class="form-group">
            <label>Bio</label>
            <textarea v-model="editData.bio" rows="3"></textarea>
          </div>

          <div class="form-group">
            <label>Interests / Hobbies</label>
            <input v-model="editData.hobbie1" type="text" placeholder="Interest 1" />
            <input v-model="editData.hobbie2" type="text" placeholder="Interest 2" class="mt-8" />
            <input v-model="editData.hobbie3" type="text" placeholder="Interest 3" class="mt-8" />
          </div>

          <div class="form-group">
            <label>Looking For</label>
            <select v-model="editData.relationship_goal">
              <option value="Relationship">Relationship</option>
              <option value="Friendship">Friendship</option>
              <option value="Casual">Casual</option>
              <option value="Any">Any</option>
            </select>
          </div>

          <div class="form-group">
            <label>Profile Visibility</label>
            <select v-model="editData.visibility">
              <option value="public">Public</option>
              <option value="private">Private</option>
            </select>
          </div>

          <div class="form-group">
            <label>Profile Picture</label>
            <input type="file" accept="image/jpeg,image/png,image/jpg" @change="handleFileChange" />
          </div>

          <div class="btn-row">
            <button type="submit" class="btn-save" :disabled="isSaving">
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
            <button type="button" class="btn-cancel" @click="cancelEdit">Cancel</button>
          </div>
        </form>
      </div>
    </template>

    <div v-if="!user && !isEditing" class="loading">
      <p>Loading your profile...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';

const user = ref(null);
const isEditing = ref(false);
const isSaving = ref(false);
const saveError = ref('');
const saveSuccess = ref('');
const newPicFile = ref(null);

const editData = reactive({
  first_name: '',
  last_name: '',
  age: '',
  gender: '',
  location: '',
  bio: '',
  hobbie1: '',
  hobbie2: '',
  hobbie3: '',
  relationship_goal: '',
  visibility: 'public'
});

const picUrl = computed(() => {
  if (!user.value?.pic || user.value.pic === 'default.png') return null;
  return 'http://localhost:5000/static/uploads/' + user.value.pic;
});

async function fetchMyProfile() {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch("http://localhost:5000/api/v1/profile", {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    if (response.ok) {
      user.value = data;
    }
  } catch (error) {
    console.error("Network error:", error);
  }
}

function startEdit() {
  Object.assign(editData, {
    first_name: user.value.first_name,
    last_name: user.value.last_name,
    age: user.value.age || '',
    gender: user.value.gender || '',
    location: user.value.location || '',
    bio: user.value.bio || '',
    hobbie1: user.value.hobbie1 || '',
    hobbie2: user.value.hobbie2 || '',
    hobbie3: user.value.hobbie3 || '',
    relationship_goal: user.value.relationship_goal || '',
    visibility: user.value.visibility || 'public'
  });
  saveError.value = '';
  saveSuccess.value = '';
  isEditing.value = true;
}

function cancelEdit() {
  isEditing.value = false;
  newPicFile.value = null;
}

function handleFileChange(event) {
  newPicFile.value = event.target.files[0] || null;
}

async function saveProfile() {
  saveError.value = '';
  saveSuccess.value = '';
  isSaving.value = true;

  const body = new FormData();
  Object.entries(editData).forEach(([key, val]) => body.append(key, val));
  if (newPicFile.value) {
    body.append('profile_pic', newPicFile.value);
  }

  try {
    const token = localStorage.getItem('token');
    const response = await fetch("http://localhost:5000/api/v1/profile", {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` },
      body
    });
    const data = await response.json();
    if (response.ok) {
      saveSuccess.value = 'Profile updated!';
      await fetchMyProfile();
      setTimeout(() => { isEditing.value = false; saveSuccess.value = ''; }, 1000);
    } else {
      saveError.value = data.error || 'Failed to save changes.';
    }
  } catch (error) {
    saveError.value = 'Could not connect to server.';
  } finally {
    isSaving.value = false;
  }
}

onMounted(fetchMyProfile);
</script>

<style scoped>
.profile-container { max-width: 800px; margin: 40px auto; padding: 20px; }

.profile-header { text-align: center; margin-bottom: 30px; }
.pic-wrapper { display: inline-block; }
.main-pic { width: 180px; height: 180px; border-radius: 50%; object-fit: cover; border: 5px solid #6366f1; }
.placeholder-pic {
  width: 180px; height: 180px; border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; font-size: 3rem; font-weight: 700;
  display: inline-flex; align-items: center; justify-content: center;
  margin: 0 auto;
}
.username { color: #666; font-style: italic; }
.tagline { color: #888; font-size: 0.9rem; margin-top: 4px; }

.btn-edit {
  margin-top: 12px; padding: 10px 28px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; border: none; border-radius: 8px;
  font-weight: 600; cursor: pointer;
}

.profile-details { display: grid; gap: 20px; }
.detail-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
h3 { color: #6366f1; margin-top: 0; }

.hobbies { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { background: #ede9fe; color: #6366f1; padding: 4px 14px; border-radius: 20px; font-size: 0.9rem; }
.no-data { color: #aaa; font-style: italic; }

/* Edit form */
.edit-card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
h2 { color: #6366f1; margin-bottom: 1.5rem; }
form { display: flex; flex-direction: column; gap: 16px; }

.form-group { display: flex; flex-direction: column; gap: 4px; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #555; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.mt-8 { margin-top: 8px; }

input, select, textarea {
  padding: 10px 12px; border: 1px solid #d1d5db;
  border-radius: 8px; font-size: 0.95rem;
  width: 100%; box-sizing: border-box;
}
input:focus, select:focus, textarea:focus {
  outline: none; border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}
textarea { resize: vertical; }

.btn-row { display: flex; gap: 12px; margin-top: 8px; }
.btn-save {
  flex: 1; padding: 12px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;
}
.btn-cancel {
  flex: 1; padding: 12px; background: #f3f4f6;
  color: #555; border: 1px solid #d1d5db;
  border-radius: 8px; font-weight: 600; cursor: pointer;
}
.btn-save:disabled { opacity: 0.7; cursor: not-allowed; }

.alert { padding: 10px; border-radius: 5px; margin-bottom: 12px; }
.alert-success { background: #d4edda; color: #155724; }
.alert-danger { background: #f8d7da; color: #721c24; }

.loading { text-align: center; color: #888; margin-top: 60px; }
</style>