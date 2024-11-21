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
    <div class="component-wrapper" style="color: aliceblue;">
        <router-link to="/sponsorlogin" class="back-button">
            <i class="fas fa-arrow-circle-left"></i>
        </router-link>
        <div class="overlay">
            <div class="register">
                <div class="container">
                    <h3 class="text-center">Sponsor Registration</h3>
                    <form class="text-center" @submit.prevent="validateForm">
    <div v-if="errors.general" class="text-danger">{{ errors.general }}</div>
    <div class="mb-3">
        <input type="text" class="form-control form-control-sm" style="height:35px; position:relative; bottom:-5px;" placeholder="Username" v-model="sponsorname">
    </div>
    <div class="mb-3">
        <input type="email" class="form-control form-control-sm" style="height:35px; position:relative; bottom:0px;" placeholder="Email Address" v-model="email">
    </div>
    <div class="mb-3">
        <input type="password" class="form-control form-control-sm" style="height:35px; position:relative; bottom:0px;" placeholder="Password" v-model="password">
    </div>
    <div class="mb-3 select-wrapper">
        <select class="form-control form-control-sm" v-model="industry" style="height:35px; position:relative; bottom:5px; padding:0px; padding-left:15px;">
            <option value="" disabled>Select your industry</option>
            <option value="Technology">Technology</option>
            <option value="Fashion">Fashion</option>
            <option value="Health">Health</option>
            <option value="Beauty">Beauty</option>
            <option value="Fitness">Fitness</option>
            <option value="Food">Food</option>
            <option value="Travel">Travel</option>
            <option value="Gaming">Gaming</option>
            <option value="Lifestyle">Lifestyle</option>
            <option value="Education">Education</option>

            <!-- <option value="Automotive">Automotive</option> -->
            <!-- <option value="Finance">Finance</option> -->
            <!-- Fashion, Beauty, Fitness, Food, Travel, Gaming, Technology, Lifestyle, Education, Health -->
        </select>
    </div>
    <div class="mb-3">
        <input type="text" class="form-control form-control-sm" style="height:35px; position:relative; bottom:10px;" placeholder="Company Name" v-model="companyName">
    </div>
    <div class="mb-3">
        <input type="text" class="form-control form-control-sm" style="height:35px; position:relative; bottom:10px;" placeholder="Company Website" v-model="companyWebsite">
    </div>
    <div class="mb-3">
        <input type="text" class="form-control form-control-sm" style="height:35px; position:relative; bottom:10px;" placeholder="Contact Number" v-model="contactNumber">
    </div>
    <button type="submit" class="btn btn-outline-light mb-3">Register</button>
    <div class="d-flex justify-content-center align-items-center">
        <p class="mb-0 me-2">Already have an account?</p>
        <router-link to="/sponsorlogin" class="text-link">Login</router-link>
    </div>
</form>

                </div>
            </div>
        </div>
    </div></div></div>
</template>

<script>
import shared from '../shared';

export default {
  data() {
    return {
      sponsorname: shared.formData.sponsorname || '',
      email: shared.formData.email || '',
      password: shared.formData.password || '',
      industry: shared.formData.industry || '',
      companyName: shared.formData.companyName || '',
      companyWebsite: shared.formData.companyWebsite || '',
      contactNumber: shared.formData.contactNumber || '',
      feedbackColor: '',
      feedbackMessage: '',
      errors: {
        general: ''
      }
    };
  },
  methods: {
    validateForm() {
      this.clearErrors();
      if (!this.sponsorname || !this.email || !this.password || !this.industry || !this.companyName || !this.companyWebsite || !this.contactNumber) {
        this.errors.general = 'All fields are required';
      } else {
        shared.formData = {
          sponsorname: this.sponsorname,
          email: this.email,
          password: this.password,
          industry: this.industry,
          companyName: this.companyName,
          companyWebsite: this.companyWebsite,
          contactNumber: this.contactNumber
        };
        this.$router.push('/sponsorconfirm');
      }
    },
    clearErrors() {
      this.errors = { general: '' };
    }
  }
};
</script>

<style>
.select-wrapper {
    position: relative;
    display: inline-block;
    width: 100%;
}

.select-wrapper select {
    width: 100%;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background: none;
    border: 1px solid #ccc;
    padding: 0.5rem;
    padding-right: 2.5rem;
    border-radius: 4px;
    height: 35px;
}

.select-wrapper::after {
    content: '\f078';
    font-family: 'Font Awesome 5 Free';
    font-weight: 900;
    position: absolute;
    top: 25%;
    right: 17.5px;
    transform: translateY(-50%);
    pointer-events: none;
    color: #545454;
}

.form-control-sm {
    font-size: 0.875rem;
    height: 35px;
}
</style>