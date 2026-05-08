<template>
    <div class="page-wrapper">
        <div class="register-card">
            <h1>Registration Form</h1>
            
            <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
            <div v-if="errorMessages.length" class="alert alert-danger">
                <ul>
                    <li v-for="error in errorMessages" :key="error">{{ error }}</li>
                </ul>
            </div>

            <form id="registrationForm" @submit.prevent="handleRegister">
                <input v-model="formData.username" type="text" placeholder="Username" required />
                <input v-model="formData.email" type="email" placeholder="Email" required />
                <input v-model="formData.password" type="password" placeholder="Password" required />
                
                <input v-model="formData.first_name" type="text" placeholder="First Name" />
                <input v-model="formData.last_name" type="text" placeholder="Last Name" />

                <button type="submit">Register</button>
            </form>
        </div>
    </div>
</template>

<script setup>
    import { ref, reactive } from 'vue';

    const formData = reactive({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        bio: ''
    });

    const successMessage = ref('');
    const errorMessages = ref([]);

    async function handleRegister() {
        successMessage.value = "";
        errorMessages.value = [];

        try {
            // UPDATED: Points to your Flask API with the v1 prefix
            const response = await fetch("http://localhost:5000/api/v1/register", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData) 
            });

            const data = await response.json();

            if (!response.ok) {
                // Flask sends errors as {"errors": ["..."]} or {"error": "..."}
                errorMessages.value = data.errors || [data.error] || ["An unknown error occurred."];
            } else {
                successMessage.value = data.message;
                // Reset form
                formData.username = '';
                formData.email = '';
                formData.password = '';
                formData.first_name = '';
                formData.last_name = '';
            }
        } catch (error) {
            console.error("Fetch error:", error);
            errorMessages.value = ["Could not connect to the Flask server. Make sure it is running!"];
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
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

#registrationForm {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* Simple styling for the error/success messages */
.alert {
    padding: 10px;
    margin-bottom: 15px;
    border-radius: 5px;
}
.alert-success { background-color: #d4edda; color: #155724; }
.alert-danger { background-color: #f8d7da; color: #721c24; text-align: left; }
</style>
