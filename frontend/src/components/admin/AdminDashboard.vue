<template>
  <div class="app-container" style="overflow-y: auto; color: lightseagreen;">
    <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-dark shadow-sm">
      <div class="container-fluid">
        <router-link :to="'/a/dashboard/'+username" class="navbar-brand" style="color: #fff;">Admin Dashboard</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto" style="position: relative; right: 70px;">
            <li class="nav-item">
              <router-link :to="'/a/dashboard/'+username" class="nav-link" style="color: #fff;">Dashboard Info</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="'/a/'+username+'/applications'" class="nav-link" style="color: #fff;">Applications</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="'/a/'+username+'/find'" class="nav-link" style="color: #fff;">Find</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="'/a/'+username+'/stats'" class="nav-link" style="color: #fff;">Stats</router-link>
            </li>
            <li class="nav-item">
              <a @click="logout" class="nav-link" style="cursor: pointer; color: #fff;">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
      <div class="container mt-4" style="flex-grow: 1; position: relative; top: 50px;">
        <h1 class="display-4">Greetings, {{ username }}!</h1>
        <p class="lead">Welcome to your admin dashboard.</p>
        <hr class="my-4">
        <div class="row text-center mb-4" style="display: flex; justify-content: space-around;">
          <h5 style="display: flex; justify-content: left;">General Overview</h5>
          <div class="col-md-4" style="flex: 1; margin: 0 10px;">
            <div class="card shadow-sm" style="border: none; border-radius: 12px;">
              <div class="card-body" style="text-align: center;">
                <h5 class="card-title" style="font-weight: bold; font-size: 1.2rem;">Total Users</h5>
                <p class="card-text display-4" style="font-size: 2.5rem; font-weight: bold; color: #007bff;">{{totalUsers}}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4" style="flex: 1; margin: 0 10px;">
            <div class="card shadow-sm" style="border: none; border-radius: 12px;">
              <div class="card-body" style="text-align: center;">
                <h5 class="card-title" style="font-weight: bold; font-size: 1.2rem;">Total Sponsors</h5>
                <p class="card-text display-4" style="font-size: 2.5rem; font-weight: bold; color: #007bff;">{{totalSponsors}}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4" style="flex: 1; margin: 0 10px;">
            <div class="card shadow-sm" style="border: none; border-radius: 12px;">
              <div class="card-body" style="text-align: center;">
                <h5 class="card-title" style="font-weight: bold; font-size: 1.2rem;">Total Campaigns</h5>
                <p class="card-text display-4" style="font-size: 2.5rem; font-weight: bold; color: #007bff;">{{totalCampaigns}}</p>
              </div>
            </div>
          </div>
        </div>
        <hr style="width: 40%;">
        <div class="ongoing-campaigns mb-4">
          <h5>Ongoing Campaigns</h5>
          <div v-if="ongoingCampaigns.length === 0" class="alert alert-warning">No ongoing campaigns</div>
        <ul class="list-group">
          <li v-for="campaign in ongoingCampaigns" :key="campaign.campaign_id" class="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <h5><strong>Campaign Name: </strong>{{ campaign.campaign_name }}</h5>
              <strong>By: </strong>{{ campaign.sponsor_id }}
            </div>
            <div>
              <button @click="viewCampaign(campaign)" class="btn btn-primary btn-sm">View</button>
              <button @click="confirmDelete('campaign', campaign.campaign_id)" class="btn btn-danger btn-sm">Delete</button>
              <button v-if="!campaign.flagged" @click="flagCampaign(campaign.campaign_id)" class="btn btn-warning btn-sm">Flag</button>
              <button v-else @click="unflagCampaign(campaign.campaign_id)" class="btn btn-secondary btn-sm">Unflag</button>
            </div>
          </li>
        </ul>
      </div>

      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title" style="color:slategray;">Campaign Details</h4>
            <button type="button" class="btn-close" @click="showModal = false" style="position:absolute; right: 5%;"></button>
          </div>
          <hr style="width: 100%; margin: 0; padding-bottom: 5%; color:gray;">
          <div class="modal-body">
            <p><strong style="color: lightsteelblue;">Campaign Name:</strong> {{ selectedCampaign?.campaign_name }}</p>
            <p><strong style="color: lightsteelblue;">Ad Title:</strong> {{ selectedCampaign?.ad_title }}</p>
            <p><strong style="color: lightsteelblue;">Ad Description:</strong> {{ selectedCampaign?.ad_description }}</p>
            <p><strong style="color: lightsteelblue;">Terms and Conditions:</strong> {{ selectedCampaign?.terms_and_conditions }}</p>
            <p><strong style="color: lightsteelblue;">Start Date:</strong> {{ selectedCampaign?.start_date }}</p>
            <p><strong style="color: lightsteelblue;">End Date:</strong> {{ selectedCampaign?.end_date }}</p>
            <p><strong style="color: lightsteelblue;">Payment:</strong> {{ selectedCampaign?.payment }}</p>
            <p><strong style="color: lightsteelblue;">Is Active:</strong> {{ selectedCampaign?.is_active }}</p>
            <p><strong style="color: lightsteelblue;">Is Private:</strong> {{ selectedCampaign?.is_private }}</p>
            <p><strong style="color: lightsteelblue;">Flagged:</strong> {{ selectedCampaign?.flagged }}</p>
          </div>
          <!-- <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Close</button>
          </div> -->
        </div>
      </div>
        
        <hr style="width: 25%;">
        <div class="new-requests" style="margin-top: 30px; max-height: 300px; overflow-y: auto;">
          <h5 style="margin-bottom: 20px;">Flagged/ Banned Users</h5>
          <div v-if="newRequests.length === 0" class="alert ">No Banned User</div>
          <ul class="list-group">
            <li v-for="request in newRequests" :key="request.id" class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h5 style="margin: 0;">Username: <small class="text-muted">{{request.username}}</small></h5>
              </div>
              <div>
                <button @click="confirmDelete('user', request.id)" class="btn btn-danger btn-sm" style="margin-left: 5px;">Delete</button>
                <button class="btn btn-sm ms-2" :class="{'btn-danger': request?.is_banned, 'btn-success': !request?.is_banned}" @click="toggleBan(request, 'user')">
                  {{ request?.is_banned ? 'Unban' : 'Ban' }}
                </button>
              </div>
            </li>
          </ul>
        </div>
        <div class="sponsor_action" style="margin-top: 30px; max-height: 300px; overflow-y: auto;">
          <h5 style="margin-bottom: 20px;">Flagged/ Banned Sponsors</h5>
          <div v-if="sponsor_action.length === 0" class="alert">No Banned Sponsor</div>
          <ul class="list-group">
            <li v-for="request in sponsor_action" :key="request.sponsor_id" class="list-group-item d-flex justify-content-between align-items-center" style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #dee2e6; border-radius: 12px; margin-bottom: 10px; padding: 15px; background-color: #fff;">
              <div>
                <h5 style="margin: 0;">Sponsor Name: <small class="text-muted">{{request.sponsor_name}}</small></h5>
              </div>
              <div>
                <button @click="confirmDelete('sponsor', request.sponsor_id)" class="btn btn-danger btn-sm" style="margin-left: 5px;">Delete</button>
                <button class="btn btn-sm ms-2" :class="{'btn-danger': request?.is_banned, 'btn-success': !request?.is_banned}" @click="toggleBan(request, 'sponsor')">
                  {{ request?.is_banned ? 'Unban' : 'Ban' }}
                </button>
              </div>
            </li>
          </ul>
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
      totalUsers: 0,
      totalSponsors: 0,
      totalCampaigns: 0,
      ongoingCampaigns: [],
      newRequests: [],
      sponsor_action: [],
      showModal: false,
      selectedCampaign: null,
      access_token: localStorage.getItem('access_token'),
      role_id: localStorage.getItem('role_id'),
      storedusername: localStorage.getItem('username'),
      theme: localStorage.getItem('theme') || 'light',
    };
  },
  created() {
    if (!this.access_token || this.role_id !== '1' || this.storedusername !== this.username) {
      this.$router.push('/login');
    } else {
      this.fetchData();
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(`/api/a/dashboard/${this.username}`);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("Fetched data:", data);
        this.totalUsers = data.totalUsers || 0;
        this.totalSponsors = data.totalSponsors || 0;
        this.totalCampaigns = data.totalCampaigns || 0;
        this.ongoingCampaigns = data.ongoingCampaigns || [];
        this.newRequests = data.newRequests || [];
        this.sponsor_action = data.sponsor_action || [];
      } catch (error) {
        console.error("Fetch error:", error);
      }
    },
    viewCampaign(campaign) {
      this.selectedCampaign = campaign;
      this.showModal = true;
    },
    toggleBan(item, type) {
      axios.post(`/api/a/dashboard/${this.username}`, {
        id: type === 'user' ? item.id : item.sponsor_id,
        type: type,
        action: item.is_banned ? 'unban' : 'ban'
      })
      .then(() => {
        if (type === 'user') {
          item.is_banned = !item.is_banned;
        } else if (type === 'sponsor') {
          item.is_banned = !item.is_banned;
        }
      }).then(() =>{this.fetchData();})
      .catch(error => {
        console.error('Error toggling ban status:', error);
      });
    },
    async confirmDelete(type, id) {
      const confirmation = window.confirm(`Are you sure you want to delete this ${type}? This action cannot be undone. All the data associated with this ${type} will be lost.`);
      if (confirmation) {
        try {
          await axios.delete(`/api/a/dashboard/${this.username}`, {
            data: {
              id: id,
              type: type
            }
          });
          alert(`${type.charAt(0).toUpperCase() + type.slice(1)} with ID ${id} has been deleted.`);
          await this.fetchData(); 
        } catch (error) {
          console.error('Error deleting item:', error);
        }
      }
    },
    async flagCampaign(campaignId) {
      try {
        await axios.post(`/api/a/dashboard/${this.username}`, {
          id: campaignId,
          type: 'campaign',
          action: 'flag'
        });
        await this.fetchData();
      } catch (error) {
        console.error('Error flagging campaign:', error);
      }
    },
    async unflagCampaign(campaignId) {
      try {
        await axios.post(`/api/a/dashboard/${this.username}`, {
          id: campaignId,
          type: 'campaign',
          action: 'unflag'
        });
        await this.fetchData();
      } catch (error) {
        console.error('Error unflagging campaign:', error);
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push('/login');
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
  padding-left: 5px;
  padding-right: 0;
}

.container {
  margin-top: 56px; 
  padding: 20px;
}

.modal-overlay {
  /* position: fixed; */
  top: 0;
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  border-radius: 5px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  padding: 20px;
  width: 80%;
  max-width: 500px;
}
</style>