<template>
    <div class="full-height d-flex align-items-center">
      <div class="welcome-section text-center">
        <h1>Welcome to SponsorNet</h1>
      </div>
      <div class="divider"></div>
      <div class="login-section" style="color: aliceblue;">

        <h2 class="mb-3 text-center" style="position: relative; bottom: 5px; margin: 0">Register</h2>
        <router-link to="/login" class="back-button" style="position: relative; top: -80px; right: -180px;">
          <i class="fas fa-arrow-circle-left" ></i>
        </router-link>
        <div v-if="feedbackMessage" :class="['alert', feedbackColor]" role="alert" style="margin: 0; padding: 0; position: relative; top: -15px;">
          {{ feedbackMessage }}
        </div>
        <form class="text-center" @submit.prevent="validateForm" style="height: 70vh; position: relative;">
          <div class="mb-3">
            <input type="text" class="form-control form-control-sm" placeholder="Username" v-model="username" style="height: 20px; position: relative; bottom: 10px;">
            <span class="text-danger">{{ errors.username }}</span>
          </div>
          <div class="mb-3">
            <input type="email" class="form-control form-control-sm" placeholder="Email" v-model="email" style="height: 20px; position: relative; bottom: 10px;">
            <span class="text-danger">{{ errors.email }}</span>
          </div>
          <div class="mb-3">
            <input type="password" class="form-control form-control-sm" placeholder="Password" v-model="password" style="height: 20px; position: relative; bottom: 10px;">
            <span class="text-danger">{{ errors.password }}</span>
          </div>
          <div class="mb-3 select-wrapper" style="position: center; bottom: 10px;">
            <select class="form-control form-control-sm" v-model="niche" style="height: 30px; position: relative; padding: 0px; padding-left: 15px;">
              <option value="" disabled>Select your niche</option>
              <option value="fashion">Fashion</option>
              <option value="beauty">Beauty</option>
              <option value="fitness">Fitness</option>
              <option value="food">Food</option>
              <option value="travel">Travel</option>
              <option value="gaming">Gaming</option>
              <option value="technology">Technology</option>
              <option value="lifestyle">Lifestyle</option>
              <option value="education">Education</option>
              <option value="health">Health</option>
            </select>
          </div>
          <p class="text" style="height: 20px; position: relative; bottom: 40px; top: -40px; color:lightcyan;">Adding your social media links is recommended to attract sponsors!</p>
          <div class="mb-3 d-flex align-items-center" style="margin-bottom: 15px;">
            <i class="fab fa-instagram social-media-icon" style="height: 20px; position: relative; bottom: 25px; right: 10px;"></i>
            <input type="text" class="form-control form-control-sm" placeholder="Instagram URL" v-model="instagram" style="height: 15px; position: relative; bottom: 20px; max-width: 280px; ">
          </div>
          <div class="mb-3 d-flex align-items-center" style="margin-bottom: 15px;">
            <i class="fab fa-youtube social-media-icon" style="height: 20px; position: relative; bottom: 40px; right: 10px"></i>
            <input type="text" class="form-control form-control-sm" placeholder="YouTube URL" v-model="youtube" style="height: 15px; position: relative; bottom: 35px; max-width: 280px;">
          </div>
          <div class="mb-3 d-flex align-items-center">
            <img src="@/assets/icons/x-twitter-brands-solid.svg" alt="Twitter" class="social-media-icon twitter" style="height: 15px; position: relative; bottom: 60px; right: 10px; color: white;">
            <input type="text" class="form-control form-control-sm" placeholder="Twitter URL" v-model="twitter" style="height: 20px; position: relative; bottom: 50px; max-width: 280px;">
          </div>
          <button type="submit" class="btn btn-outline-light mb-3" style="position: relative; bottom: 60px;">Register</button>
          <div class="d-flex justify-content-center align-items-center">
            <p class="mb-0 me-2" style="position: relative; bottom: 60px;">Already have an account?</p>
            <router-link to="/login" class="text-link" style="position: relative; bottom: 60px;">Login</router-link>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
        niche: '',
        instagram: '',
        youtube: '',
        twitter: '',
        errors: {
          username: '',
          email: '',
          password: ''
        },
        feedbackMessage: '',
        feedbackColor: ''
      };
    },
    methods: {
  capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  },
  validateForm() {
    const formData = {
      username: this.username,
      email: this.email,
      password: this.password,
      niche: this.capitalizeFirstLetter(this.niche),
      social_media: {
        instagram: this.instagram,
        youtube: this.youtube,
        twitter: this.twitter
      }
    };
    console.log(formData);
    axios.post('http://localhost:8080/api/register', formData)
    .then(response => {
      if (response.data.error) {
        this.feedbackMessage = response.data.error;
        this.feedbackColor = 'text-danger';
      } else {
        this.feedbackMessage = response.data.message;
        this.feedbackColor = 'text-success';
      }
    })
    .catch(error => {
      if (error.response && error.response.status === 400) {
        this.feedbackMessage = error.response.data.error;
      } else {
        console.error('Error:', error);
        this.feedbackMessage = 'An error occurred while registering.';
      }
      this.feedbackColor = 'text-danger';
    });
  }
}};
  </script>
  
<style scoped>
  .social-media-icon {
    width: 1.5rem;
    height: 1.0rem;
    margin-right: 0.5rem;
  }
  
  .social-media-icon.twitter {
    width: 1.5rem;
    height: 1.0rem;
    margin-right: 0.5rem;
  }
  
  .position-relative {
    position: relative;
  }
  
  .dropdown-arrow {
    position: relative;
    right: 10px;
    top: 30%;
    transform: translateY(-30%);
    pointer-events: none;
  }
  </style>