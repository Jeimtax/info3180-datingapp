<template>
    <div class="page-wrapper">
        <div class="register-card">
            <h1>Sign Up</h1>

            <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
            <div v-if="errorMessages.length" class="alert alert-danger">
                <ul>
                    <li v-for="error in errorMessages" :key="error">{{ error }}</li>
                </ul>
            </div>

            <form id="registrationForm" @submit.prevent="handleRegister">
                <div class="form-group">
                    <label>Email</label>
                    <input v-model="formData.email" type="email" placeholder="your@email.com" required />
                </div>

                <div class="form-group">
                    <label>Username</label>
                    <input v-model="formData.username" type="text" placeholder="username" required />
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>First Name</label>
                        <input v-model="formData.first_name" type="text" placeholder="First Name" required />
                    </div>
                    <div class="form-group">
                        <label>Last Name</label>
                        <input v-model="formData.last_name" type="text" placeholder="Last Name" required />
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>Date of Birth</label>
                        <input v-model="formData.age" type="number" placeholder="Age" min="18" max="99" required />
                    </div>
                    <div class="form-group">
                        <label>Gender</label>
                        <select v-model="formData.gender" required>
                            <option value="">Select gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Non-binary">Non-binary</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label>Looking For</label>
                    <select v-model="formData.relationship_goal" required>
                        <option value="">Select...</option>
                        <option value="Relationship">Relationship</option>
                        <option value="Friendship">Friendship</option>
                        <option value="Casual">Casual</option>
                        <option value="Any">Any</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Location</label>
                    <input v-model="formData.location" type="text" placeholder="City, Country" required />
                </div>

                <div class="form-group">
                    <label>Bio</label>
                    <textarea v-model="formData.bio" placeholder="Tell us about yourself..." rows="3"></textarea>
                </div>

                <div class="form-group">
                    <label>Interests / Hobbies</label>
                    <input v-model="formData.hobbie1" type="text" placeholder="Interest 1" required />
                    <input v-model="formData.hobbie2" type="text" placeholder="Interest 2" required class="mt-8" />
                    <input v-model="formData.hobbie3" type="text" placeholder="Interest 3" required class="mt-8" />
                </div>

                <div class="form-group">
                    <label>Profile Picture</label>
                    <input type="file" accept="image/jpeg,image/png,image/jpg" @change="handleFileChange" />
                </div>

                <div class="form-group">
                    <label>Profile Visibility</label>
                    <select v-model="formData.visibility">
                        <option value="public">Public</option>
                        <option value="private">Private</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input v-model="formData.password" type="password" placeholder="Password" required />
                </div>

                <button type="submit" :disabled="isLoading">
                    {{ isLoading ? 'Signing up...' : 'Sign Up' }}
                </button>

                <p class="login-link">Already have an account? <router-link to="/login">Login here</router-link></p>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoading = ref(false);
const profilePicFile = ref(null);

const formData = reactive({
    username: '',
    email: '',
    password: '',
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

const successMessage = ref('');
const errorMessages = ref([]);

function handleFileChange(event) {
    profilePicFile.value = event.target.files[0] || null;
}

async function handleRegister() {
    successMessage.value = '';
    errorMessages.value = [];
    isLoading.value = true;

    const body = new FormData();
    Object.entries(formData).forEach(([key, val]) => body.append(key, val));
    if (profilePicFile.value) {
        body.append('profile_pic', profilePicFile.value);
    }

    try {
        const response = await fetch("http://localhost:5000/api/v1/register", {
            method: 'POST',
            body
        });

        const data = await response.json();

        if (!response.ok) {
            errorMessages.value = data.errors || [data.error] || ["An unknown error occurred."];
        } else {
            successMessage.value = data.message;
            setTimeout(() => router.push('/login'), 1500);
        }
    } catch (error) {
        console.error("Fetch error:", error);
        errorMessages.value = ["Could not connect to the Flask server. Make sure it is running!"];
    } finally {
        isLoading.value = false;
    }
}
</script>

<style scoped>
.page-wrapper {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    background-color: #f5f7fa;
    padding: 40px 16px;
}

.register-card {
    background: white;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 480px;
}

h1 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #6366f1;
}

#registrationForm {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.form-group label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #555;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.mt-8 { margin-top: 8px; }

input, select, textarea {
    padding: 10px 12px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 0.95rem;
    width: 100%;
    box-sizing: border-box;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

textarea { resize: vertical; }

button[type="submit"] {
    padding: 12px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 8px;
}

button:disabled { opacity: 0.7; cursor: not-allowed; }

.login-link {
    text-align: center;
    font-size: 0.9rem;
    color: #666;
}

.login-link a { color: #6366f1; text-decoration: none; }

.alert { padding: 10px; margin-bottom: 15px; border-radius: 5px; }
.alert-success { background-color: #d4edda; color: #155724; }
.alert-danger { background-color: #f8d7da; color: #721c24; }
.alert-danger ul { margin: 0; padding-left: 16px; }
</style>