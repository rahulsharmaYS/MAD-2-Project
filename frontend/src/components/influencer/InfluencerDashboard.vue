<template>
  <div class="app-container" :class="{ 'dark-theme': theme === 'dark', 'light-theme': theme === 'light' }" style="background: transparent; color: lightseagreen; overflow-y: auto;">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link class="navbar-brand" :to="'/u/dashboard/'+username" style="position: relative; left: 10px;">SponsorNet</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'dashboard', params: { username: username } }">Your Dashboard</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto" style="position: relative; right: 100px;">
            <li class="nav-item">
              <router-link :to="'/u/'+username + '/profile'" class="nav-link">Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="'/u/'+username+'/find'">Search Users</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="'/u/'+username+'/findcampaigns'">Find Campaigns</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="'/u/'+username+'/stats'">Stats</router-link>
            </li>
            <li class="nav-item">
              <a @click="logout" class="nav-link" style="cursor: pointer;">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div style="position: relative; top: 50px;">
      <h1 class="text-center mt-4" style="position: relative; left: -510px;">Welcome, {{ username }}!</h1>
      <hr width="60%" style="position: relative; left: 90px;">
      
      <!-- Active Campaigns Section -->
      <div class="container mt-4">
        <h3>Active Campaigns</h3>
        <small style="color: red;"><i>Warning, if the campaign is cancelled then it will be deleted permanently. Doing regularly might lead to ban!</i></small>
        <div v-if="filteredCampaigns.length === 0">
          <p>No campaigns available</p>
        </div>
        <div v-else class="campaign-slider-wrapper">
          <button class="slider-control prev" @click="scrollLeft">‹</button>
          <div class="campaign-slider">
            <div v-for="campaign in filteredCampaigns" :key="campaign.campaign_req_id" class="campaign-card">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title"><strong>Campaign Name:</strong> {{ campaign.campaign_name }}</h5>
                  <p class="card-text"><strong>Ad Title: </strong>{{ campaign.ad_title }}</p>
                  <p class="card-text"><strong>Ad Description: </strong>{{ campaign.ad_description }}</p>
                  <p class="card-text">Price: {{ campaign.negotiated_price }}</p>
                  <p class="card-text">Status: {{ campaign.status }}</p>
                  <p class="card-text">Sponsor Name: {{ campaign.sponsor_id }}</p>
                  <p class="card-text">Terms and Condition: {{ campaign.terms_and_conditions }}</p>
                  <p class="card-text">Start Date: {{ campaign.start_date }}</p>
                  <p class="card-text">End Date: {{ campaign.end_date }}</p>
                  <button @click="cancelCampaign(campaign.campaign_req_id)" class="btn btn-danger">Cancel</button>
                </div>
              </div>
            </div>
          </div>
          <button class="slider-control next" @click="scrollRight">›</button>
        </div>
      </div>

      <hr width="60%" style="position: relative; left: 90px;">

      <!-- New Requests Section -->
      <div class="container mt-4" style="position: relative; height: 500px;">
        <h3>New Requests</h3>
        <small style="color: yellow;"><i>To accept the campaign request please go to findcampaigns and accept that particular request from there!</i></small>
        <div v-if="renegotiatedRequests.length === 0">
          <p>No new requests available</p>
        </div>
        <div v-else>
          <div class="campaign-slider-wrapper" style="position: relative; height: 400px; ">
            <button class="slider-control prev" @click="scrollLeft">❮</button>
            <div class="campaign-slider" style="position: relative; height: 380px; width: 35vw;">
              <div v-for="request in renegotiatedRequests" :key="request.campaign_req_id" class="campaign-card">
                <div class="card">
                  <div class="card-body">
                    <h5 class="card-title"><strong>Campaign Name:</strong> {{ request.campaign_name }}</h5>
                    <p class="card-text"><strong>Ad Title: </strong>{{ request.ad_title }}</p>
                    <p class="card-text"><strong>Ad Description: </strong>{{ request.ad_description }}</p>
                    <!-- <p class="card-text"><strong>Original Price: </strong>{{ request.payment }}</p> -->
                    <p class="card-text"><strong>Revised Price: </strong>{{ request.negotiated_price }}</p>
                    <p class="card-text"><strong>Status: </strong>{{ request.status }}</p>
                    <p class="card-text"><strong>Sponsor Name: </strong>{{ request.sponsor_id }}</p>
                    <p class="card-text"><strong>Terms and Conditions: </strong>{{ request.terms_and_conditions }}</p>
                    <p class="card-text"><strong>Start Date: </strong>{{ request.start_date }}</p>
                    <p class="card-text"><strong>End Date: </strong>{{ request.end_date }}</p>
                    <button @click="rejectRequest(request.campaign_req_id)" class="btn btn-danger">Reject</button>
                    <button @click="acceptRequest(request.campaign_req_id)" class="btn btn-success">Accept</button>
                    <button @click="showRenegotiateModal(request)" class="btn btn-warning">ReNegotiate</button>
                  </div>
                </div>
              </div>
            </div>
            <button class="slider-control next" @click="scrollRight">❯</button>
          </div>
        </div>
      </div>

      <!-- Renegotiate Modal -->
      <div v-if="showModal" class="modal fade show" tabindex="-1" style="display: block;" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Renegotiate Price</h5>
              <button type="button" class="btn-close" @click="showModal = false"></button>
            </div>
            <div class="modal-body">
              <label for="negotiatedPrice">New Price:</label>
              <input type="number" v-model="newNegotiatedPrice" class="form-control" id="negotiatedPrice" placeholder="Enter new price" />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showModal = false">Close</button>
              <button type="button" class="btn btn-primary" @click="renegotiate(requestToRenegotiate.campaign_req_id)">Save changes</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['username'],
  data() {
    return {
      token: localStorage.getItem('access_token'),
      storedUsername: localStorage.getItem('username'),
      theme: localStorage.getItem('theme') || 'light',
      campaigns: [],
      renegotiatedRequests: [],
      warningMsg: '',
      filteredCampaigns: [],
      showModal: false,
      newNegotiatedPrice: 0,
      requestToRenegotiate: {}
    };
  },
  created() {
    if (!this.token || this.username !== this.storedUsername) {
      this.$router.push('/login');
      this.warningMsg = 'Do not access other user\'s dashboard';
    } else {
      this.fetchData();
    }
  },
  methods: {
    fetchData() {
      console.log('Fetching data...');
      axios.get(`http://localhost:8080/api/u/dashboard/${this.username}`, {
        headers: { 'Authorization': `Bearer ${this.token}` }
      })
      .then(response => {
        console.log('Data fetched:', response.data);

        const { active_campaigns = [], renegotiated_requests = [] } = response.data;

        if (Array.isArray(active_campaigns)) {
          this.campaigns = active_campaigns;
          this.filteredCampaigns = this.campaigns.filter(campaign => campaign.status === 'Active');
        } else {
          console.error("Expected an array for active_campaigns but got:", active_campaigns);
          this.campaigns = [];
          this.filteredCampaigns = [];
        }

        if (Array.isArray(renegotiated_requests)) {
          this.renegotiatedRequests = renegotiated_requests;
        } else {
          console.error("Expected an array for renegotiated_requests but got:", renegotiated_requests);
          this.renegotiatedRequests = [];
        }
      })
      .catch(error => {
        console.error("There was an error fetching the data!", error);
      });
    },

    acceptRequest(campaignId) {
      axios.put(`http://localhost:8080/api/u/dashboard/${this.username}`, {
        action: 'accept',
        campaign_id: campaignId
      }, {
        headers: { 'Authorization': `Bearer ${this.token}` }
      })
      .then(() => {
        this.fetchData(); 
      })
      .catch(error => {
        console.error("There was an error accepting the campaign!", error);
      });
    },

    rejectRequest(campaignReqId) {
      axios.put(`http://localhost:8080/api/u/dashboard/${this.username}`, {
        action: 'reject',
        campaign_id: campaignReqId
      }, {
        headers: { 'Authorization': `Bearer ${this.token}` }
      })
      .then(() => {
        this.fetchData();
      })
      .catch(error => {
        console.error("There was an error rejecting the campaign!", error);
      });
    },

    renegotiate() {
      axios.put(`http://localhost:8080/api/u/dashboard/${this.username}`, {
        action: 'renegotiate',
        campaign_req_id: this.requestToRenegotiate.campaign_req_id,
        new_price: this.newNegotiatedPrice
      }, {
        headers: { 'Authorization': `Bearer ${this.token}` }
      })
      .then(() => {
        this.showModal = false;
        this.newNegotiatedPrice = 0;
        this.fetchData();
      })
      .catch(error => {
        console.error("There was an error renegotiating the campaign!", error);
      });
    },

    showRenegotiateModal(request) {
      this.requestToRenegotiate = request;
      this.showModal = true;
      this.newNegotiatedPrice = request.negotiated_price;
    },

    cancelCampaign(campaignId) {
      axios.put(`http://localhost:8080/api/u/dashboard/${this.username}`, {
        action: 'cancel',
        campaign_id: campaignId
      }, {
        headers: { 'Authorization': `Bearer ${this.token}` }
      })
      .then(() => {
        this.fetchData(); 
      })
      .catch(error => {
        console.error("There was an error cancelling the campaign!", error);
      });
    },

    logout() {
      localStorage.clear();
      this.$router.push('/');
    },

    scrollLeft() {
      const slider = this.$el.querySelector('.campaign-slider');
      slider.scrollBy({ left: -300, behavior: 'smooth' });
    },

    scrollRight() {
      const slider = this.$el.querySelector('.campaign-slider');
      slider.scrollBy({ left: 300, behavior: 'smooth' });
    },

    toggletheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', this.theme);
    }
  }
};
</script>

<style scoped>
.app-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: transparent;
  position: relative;
}

.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.navbar .container-fluid {
  max-width: 100%;
  padding-left: 0;
  padding-right: 0;
}

.container {
  margin-top: 56px;
  padding: 20px;
}

.campaign-slider-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.campaign-slider {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  white-space: nowrap;
  gap: 16px;
  padding: 0 50px;
}

.campaign-card {
  flex: 0 0 auto;
  width: 300px;
  margin-right: 16px;
  display: flex;
  flex-direction: column;
}

.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-width: 300px;
}

.card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.card-text,
.card-title {
  overflow-wrap: break-word;
  word-break: break-word;
  margin-bottom: 8px;
}

.slider-control {
  background-color: #007bff;
  border: none;
  color: white;
  font-size: 24px;
  line-height: 1;
  padding: 8px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  z-index: 1000;
  height: 48px;
  width: 48px;
}

.prev {
  left: 0;
}

.next {
  right: 0;
}

.dark-theme {
  background-color: #343a40;
  color: white;
}

.light-theme {
  background-color: #f8f9fa;
  color: black;
}

.dark-theme .card {
  border-color: #444;
}

.dark-theme .slider-control {
  background-color: #0056b3;
}
</style>