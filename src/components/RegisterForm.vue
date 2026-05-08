<template>
    <div class="page-wrapper">
        <div class="register-card">
            <h1> Registration Form</h1>
            <form id="registrationForm" @submit.prevent="handleRegister">
                <input v-model="formData.username" type="text" placeholder="Username" required />
                <input v-model="formData.email" type="email" placeholder="Email" required />
                <input v-model="formData.password" type="password" placeholder="Password" required />
            
                <button type="submit">Register</button>
            </form>

        </div>
    </div>
</template>

<script setup>
    import { ref, reactive } from 'vue';

    // 1. Define reactive data
    const formData = reactive({
    username: '',
    email: '',
    password: ''
    });

    const successMessage = ref('');
    const errorMessages = ref([]);
    const csrf_token = ref(''); // Usually passed from a global window object or a meta tag if using Flask-WTF

    async function handleRegister() {
    // Clear messages
    successMessage.value = "";
    errorMessages.value = [];

    try {
        const response = await fetch("/api/register", {
        method: 'POST',
        body: JSON.stringify(formData), // Send as JSON
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token.value // Ensure this is populated
        }
        });

        const data = await response.json();

        if (!response.ok || data.errors) {
        errorMessages.value = data.errors || ["An unknown error occurred."];
        } else {
        successMessage.value = data.message;
        // Reset form
        formData.username = '';
        formData.email = '';
        formData.password = '';
        }
    } catch (error) {
        console.error("Fetch error:", error);
        errorMessages.value = ["Could not connect to the server."];
    }
    }

</script>

<style>

.page-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa; 
}

.register-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); /* Soft shadow */
  width: 100%;
  max-width: 400px; /* Prevents it from getting too wide */
  text-align: center;
}

#registrationForm{
    display: flex;
    flex-direction: column;
    gap: 20px;
    
}

</style>