<template>
  <body style="background: transparent; width: 100vw; height: 100vh;">
    <div class="confirmation-wrapper" style="width: 100vw; height: 100vh; background: transparent;">
      <div class="confirmation-details">
        <div v-if="feedbackMessage" :class="['alert', feedbackColor]" role="alert" style="text-align:center; background:transparent; font-size:large; padding-bottom:5px; margin-bottom:0px;">
          {{ feedbackMessage }}
        </div>
        <h3 class="text-center" style="color: darkslategrey;">Confirm Your Details</h3>
        <ul class="list-group">
          <li class="list-group-item" style="background:transparent;"><strong>Username:</strong> {{ sponsorname }}</li>
          <li class="list-group-item" style="background:transparent;"><strong>Email:</strong> {{ email }}</li>
          <li class="list-group-item" style="background:transparent;"><strong>Password:</strong> {{ password }}</li>
          <li class="list-group-item" style="background:transparent;"><strong>Industry:</strong> {{ industry }}</li>
          <li class="list-group-item" style="background:transparent;"><strong>Company Name:</strong> {{ companyName }}</li>
          <li class="list-group-item" style="background:transparent; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"><strong>Company Website:</strong> {{ companyWebsite }}</li>
          <li class="list-group-item" style="background:transparent;"><strong>Contact Number:</strong> {{ contactNumber }}</li>
        </ul>
        <p class="mt-3" style="color: darkslategrey;">Are you sure you want to submit this sponsorship application?</p>
        <div class="d-flex justify-content-center">
          <button @click="confirmSubmission" class="btn btn-primary me-2">Submit</button>
          <button @click="editDetails" class="btn btn-secondary" style="background:rgba(244, 36, 36, 0.79);">Refill</button>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
import shared from '../shared';
import axios from 'axios';

export default {
  data() {
    return {
      feedbackMessage: '',
      feedbackColor: '',
      sponsorname: '',
      email: '',
      password: '',
      industry: '',
      companyName: '',
      companyWebsite: '',
      contactNumber: ''
    };
  },
  created() {
    this.sponsorname = shared.formData.sponsorname || '';
    this.email = shared.formData.email || '';
    this.password = shared.formData.password || '';
    this.industry = shared.formData.industry || '';
    this.companyName = shared.formData.companyName || '';
    this.companyWebsite = shared.formData.companyWebsite || '';
    this.contactNumber = shared.formData.contactNumber || '';
  },
  methods: {
    confirmSubmission() {
      const formData = {
        sponsorname: this.sponsorname,
        email: this.email,
        password: this.password,
        industry: this.industry,
        companyName: this.companyName,
        companyWebsite: this.companyWebsite,
        contactNumber: this.contactNumber
      };
      console.log(formData);
      axios.post('http://localhost:8080/api/sponsorconfirm', formData)
        .then(response => {
          if (response.data.error) {
            this.feedbackMessage = response.data.error;
            this.feedbackColor = 'text-danger';
            
          } else {
            this.feedbackMessage = response.data.message;
            this.feedbackColor = 'text-success';
            setTimeout(() => {
              this.$router.push({ path: `/confirmation/${this.sponsorname}` });
            }, 3000);
          }
        })
        .catch(error => {
          if (error.response && error.response.status === 400) {
            this.feedbackMessage = error.response.data.error;
          } else {
            this.feedbackMessage = 'Info exists already or wrong info is filled! Kindly refill the form';
            console.log(error);
            console.log(formData);
          }
          this.feedbackColor = 'text-danger';
        });

    },
    editDetails() {
      this.$router.push('/sponsorregister');
    }
  }
};
</script>


<style>
.confirmation-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
}
.confirmation-details {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  text-align: center;
}
.list-group-item {
  text-align: left;
}
.btn {
  margin: 5px;
}
.alert {
  margin-top: 10px;
}
</style>
