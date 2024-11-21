<template>
  <div class="full-height d-flex align-items-center">
    <div class="welcome-section text-center">
      <h1>Welcome to SponsorNet</h1>
    </div>
    <div class="divider"></div>
    <div class="login-section">
      <div v-if="feedbackMessage" :class="['alert', feedbackColor]" role="alert">
        {{ feedbackMessage }}
      </div>
      <div class="component-wrapper">
        <router-link to="/login" class="back-button">
          <i class="fas fa-arrow-circle-left"></i>
        </router-link>
        <form class="text-center" @submit.prevent="validateForm">
          <h2>Sponsor Login</h2>
          <div class="mb-3">
            <input type="text" class="form-control" placeholder="Sponsor Username" v-model="sponsorname">
            <span class="text-danger">{{ errors.sponsorname }}</span>
          </div>
          <div class="mb-3">
            <input type="password" class="form-control" placeholder="Sponsor Password" v-model="password">
            <span class="text-danger">{{ errors.password }}</span>
          </div>
          <button type="submit" class="btn btn-outline-light mb-3">Login</button>
          <div class="d-flex justify-content-center align-items-center">
            <p class="mb-0 me-2" style="color: aliceblue;">Not a sponsor yet?</p>
            <router-link to="/sponsorregister" class="text-link">Sign-Up</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sponsorname: '',
      password: '',
      errors: {
        sponsorname: '',
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
  
      if (!this.sponsorname) {
        this.errors.sponsorname = 'Sponsorname is required.';
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
        sponsorname: this.sponsorname,
        password: this.password
      };
      console.log('Login request data:', requestData);
      fetch('/api/sponsorlogin', {
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
          this.$router.push({ path: `/banned/${this.sponsorname}` });
        } else {
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('role_id', data.role_id);
          localStorage.setItem('username', this.sponsorname);
          
          this.feedbackMessage = 'Login successful!';
          this.feedbackColor = 'text-success';
          this.$router.push({ path: `/s/${this.sponsorname}/dashboard` });
        }
      })
      .catch(error => {
        console.log('Login error:', error);
        this.feedbackMessage = 'Login failed. Please try again.';
        this.feedbackColor = 'text-danger';
      });
    }
  }
};
</script>

<style scoped>
.full-height {
  height: 100vh;
}
</style>