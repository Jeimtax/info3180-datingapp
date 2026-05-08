<template>
    <div class="page-wrapper">
        <div class="login-card">
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
        </div>
    </div>
</template>

<script setup>
    import { ref, reactive } from 'vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();
    const formData = reactive({
        username: '',
        password: ''
    });

    const isLoading = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');

    async function handleLogin() {
        isLoading.value = true;
        errorMessage.value = "";
        successMessage.value = "";

        try {
            const response = await fetch("http://localhost:5000/api/v1/auth/login", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (!response.ok) {
                errorMessage.value = data.error || "Login failed. Please check your credentials.";
            } else {
                // CRITICAL: Store the JWT token in localStorage
                localStorage.setItem('token', data.token);
                
                successMessage.value = "Login successful! Redirecting...";
                
                // Wait 1 second so they see the success message, then redirect to Explore
                setTimeout(() => {
                    router.push('/explore');
                }, 1500);
            }
        } catch (error) {
            errorMessage.value = "Unable to connect to the server.";
        } finally {
            isLoading.value = false;
        }
    }
</script>

<style scoped>
/* Reusing your friend's styling for consistency */
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
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

#loginForm {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

button {
    padding: 10px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:disabled {
    background-color: #a0d9bc;
}

.alert {
    padding: 10px;
    margin-bottom: 15px;
    border-radius: 5px;
}
.alert-success { background-color: #d4edda; color: #155724; }
.alert-danger { background-color: #f8d7da; color: #721c24; }
</style>