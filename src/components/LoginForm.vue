<template>
    <div class="page-wrapper">
        <div class="login-card">

            <!-- Step 1: Username + Password -->
            <template v-if="!needs2fa">
                <h1>Login</h1>
                <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
                <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

                <form id="loginForm" @submit.prevent="handleLogin">
                    <input v-model="formData.username" type="text" placeholder="Username" required />
                    <input v-model="formData.password" type="password" placeholder="Password" required />
                    <button type="submit" :disabled="isLoading">
                        {{ isLoading ? 'Logging in...' : 'Login' }}
                    </button>
                </form>
                <p class="mt-3">
                    Don't have an account? <router-link to="/register">Register here</router-link>
                </p>
            </template>

            <!-- Step 2: 2FA Code -->
            <template v-else>
                <h1>Two-Factor Auth</h1>
                <p class="tfa-hint">Enter the 6-digit code from your authenticator app.</p>
                <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

                <form @submit.prevent="handle2fa">
                    <input
                        v-model="totpCode"
                        type="text"
                        inputmode="numeric"
                        maxlength="6"
                        placeholder="000000"
                        class="otp-input"
                        autofocus
                        required
                    />
                    <button type="submit" :disabled="isLoading">
                        {{ isLoading ? 'Verifying...' : 'Verify' }}
                    </button>
                </form>
                <button class="btn-back-link" @click="needs2fa = false; errorMessage = ''">
                    ← Back to login
                </button>
            </template>

        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const route = useRoute();
const router = useRouter();

const formData = reactive({ username: '', password: '' });
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const needs2fa = ref(false);
const pendingUserId = ref(null);
const totpCode = ref('');

async function handleLogin() {
    isLoading.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const data = await response.json();

        if (!response.ok) {
            errorMessage.value = data.error || 'Login failed. Please check your credentials.';
        } else if (data.requires_2fa) {
            pendingUserId.value = data.user_id;
            needs2fa.value = true;
        } else {
            localStorage.setItem('token', data.token);
            successMessage.value = 'Login successful! Redirecting...';
            setTimeout(() => router.push(route.query.redirect || '/explore'), 1200);
        }
    } catch {
        errorMessage.value = 'Unable to connect to the server.';
    } finally {
        isLoading.value = false;
    }
}

async function handle2fa() {
    isLoading.value = true;
    errorMessage.value = '';

    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/2fa/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: pendingUserId.value, code: totpCode.value })
        });
        const data = await response.json();

        if (!response.ok) {
            errorMessage.value = data.error || 'Verification failed.';
            totpCode.value = '';
        } else {
            localStorage.setItem('token', data.token);
            router.push(route.query.redirect || '/explore');
        }
    } catch {
        errorMessage.value = 'Unable to connect to the server.';
    } finally {
        isLoading.value = false;
    }
}
</script>

<style scoped>
.page-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
}

.login-card {
    background: white;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
    text-align: center;
}

h1 { color: #6366f1; margin-bottom: 1rem; }

form { display: flex; flex-direction: column; gap: 15px; }

input {
    padding: 10px 12px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 0.95rem;
}
input:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }

.otp-input {
    letter-spacing: 0.4em;
    font-size: 1.4rem;
    text-align: center;
    font-weight: 700;
}

button[type="submit"] {
    padding: 12px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    font-size: 1rem;
}
button:disabled { opacity: 0.7; cursor: not-allowed; }

.tfa-hint { color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem; }

.btn-back-link {
    background: none; border: none; color: #6366f1;
    cursor: pointer; font-size: 0.9rem; margin-top: 12px;
}

.mt-3 { margin-top: 1rem; font-size: 0.9rem; color: #666; }
.mt-3 a { color: #6366f1; text-decoration: none; }

.alert { padding: 10px; margin-bottom: 15px; border-radius: 5px; text-align: left; }
.alert-success { background-color: #d4edda; color: #155724; }
.alert-danger  { background-color: #f8d7da; color: #721c24; }
</style>
