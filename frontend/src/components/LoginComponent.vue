<template>
    <div class="full-height d-flex align-items-center justify-content-center">
        <div class="welcome-section text-center mb-5">
            <h1>Welcome to SponsorNet</h1>
        </div>
        <div class="divider mb-5"></div>
        <div class="login-section">
            <div v-if="feedbackMessage" :class="['alert', feedbackColor]" role="alert">
                {{ feedbackMessage }}
            </div>
            <form class="text-center" @submit.prevent="validateForm">
                <h2 class="mb-4">Login</h2>
                <div class="mb-3">
                    <input type="text" class="form-control" placeholder="Username" v-model="username">
                    <span class="text-danger">{{ errors.username }}</span>
                </div>
                <div class="mb-3">
                    <input type="password" class="form-control" placeholder="Password" v-model="password">
                    <span class="text-danger">{{ errors.password }}</span>
                </div>
                <button type="submit" class="btn btn-outline-light mb-3">Login</button>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <p class="mb-0" style="color: aliceblue;">New here?</p>
                        <router-link to="/register" class="text-link">Sign-Up</router-link>
                    </div>
                    <div>
                        <p class="mb-0" style="color: aliceblue;">Are you a sponsor?</p>
                        <router-link to="/sponsorlogin" class="text-link">Login as Sponsor</router-link>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            errors: {
                username: '',
                password: ''
            },
            feedbackMessage: '',
            feedbackColor: ''
        };
    },
    mounted() {
        const searchParams = new URLSearchParams(window.location.search);
        if (searchParams.has('message')) {
            const message = searchParams.get('message');
            this.feedbackMessage = message;
            this.feedbackColor = 'text-danger';
        }
    },
    methods: {
        validateForm() {
            this.errors = {};
            this.feedbackMessage = '';
            this.feedbackColor = '';

            if (!this.username) {
                this.errors.username = 'Username is required.';
            }

            if (!this.password) {
                this.errors.password = 'Password is required.';
            }

            if (Object.keys(this.errors).length === 0) {
                this.feedbackMessage = 'Checking credentials...';
                this.feedbackColor = 'text-primary';
                setTimeout(() => {
                    this.submitLoginForm();
                }, 1000);
            } else {
                this.feedbackMessage = 'Please fix the form errors.';
                this.feedbackColor = 'text-danger';
            }
        },
        submitLoginForm() {
            const requestData = {
            username: this.username,
            password: this.password
    };

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Login failed');
            });
        }
    })
    .then(data => {
        if (data.status === false) {
            throw new Error(data.error || 'Login failed');
        }
        if (data.is_banned) {
            this.feedbackMessage = 'Your account is banned.';
            this.feedbackColor = 'text-danger';
            this.$router.push({ path: `/banned/${data.username}` });
        } else {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('role_id', data.role_id);
            localStorage.setItem('username', data.username);

            if (data.role_id === 1) { //admin role
                this.$router.push({ path: `/a/dashboard/${data.username}` });
            } else if (data.role_id === 2) { //user role
                this.$router.push({ path: `/u/dashboard/${data.username}` });
            } else {
                throw new Error('Unexpected role ID');
            }
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        this.feedbackMessage = 'Login failed. Please try again.';
        this.feedbackColor = 'text-danger';
    });
}}
};
</script>

<style scoped>
.full-height {
    min-height: 100vh;
    overflow: hidden;
}

.welcome-section {
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.login-section {
    width: 100%;
    max-width: 400px;
    margin: auto; 
}

.text-link {
    color: #e9ecf0;
    cursor: pointer;
}

.text-link:hover {
    text-decoration: underline;
}

.alert {
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid transparent;
    border-radius: 4px;
}

.text-primary {
    color: #007bff;
}

.text-danger {
    color: #dc3545;
}

.text-success {
    color: #28a745;
}
</style>