<template>
  <div class="app-container">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
          <router-link :to="'/s/'+sponsorname+'/dashboard'" class="navbar-brand">Sponsor Dashboard</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav" style="position: relative; left: -20px;">
            <ul class="navbar-nav ms-auto" style="position: relative; right: 70px;">
              <li class="nav-item">
                <router-link :to="'/s/'+sponsorname+'/dashboard'" class="nav-link">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="'/s/'+sponsorname+'/profile'" class="nav-link">Profile</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="'/s/'+sponsorname+'/campaigns'" class="nav-link">Campaigns</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="'/s/'+sponsorname+'/find'" class="nav-link">Find</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="'/s/'+sponsorname+'/stats'" class="nav-link">Stats</router-link>
              </li>
              <li class="nav-item">
                <a @click="logout" class="nav-link" style="cursor: pointer;">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
<div class="container" style="position: relative; top: 25px;">
    <div class="header">
      <h2 style="color: aliceblue;">Campaign Management</h2>
      <hr>
      <button @click="showCreateModal = true" class="btn btn-primary">Create New Campaign</button>
    </div>

    <!-- Campaign Modal -->
    <div v-if="showCreateModal" class="modal-overlay" style="top: 50px;">
      <div class="modal-content">
        <h3 style="color: lightseagreen;">Create New Campaign</h3>
        <form @submit.prevent="createCampaign">
          <label>Campaign Name:</label>
          <input v-model="selectedCampaign.campaign_name" type="text" required>
          <label>Ad Niche:</label>
          <select v-model="selectedCampaign.ad_niche" required>
            <option disabled value="">Select Niche</option>
            <option value="Fashion">Fashion</option>
            <option value="Beauty">Beauty</option>
            <option value="Fitness">Fitness</option>
            <option value="Food">Food</option>
            <option value="Travel">Travel</option>
            <option value="Gaming">Gaming</option>
            <option value="Technology">Technology</option>
            <option value="Lifestyle">Lifestyle</option>
            <option value="Education">Education</option>
            <option value="Health">Health</option>
          </select>
          <label>Ad Description:</label>
          <textarea v-model="selectedCampaign.ad_description" required></textarea>
          <label>Terms and Conditions:</label>
          <textarea v-model="selectedCampaign.terms_and_conditions" required></textarea>
          <label>Start Date:</label>
          <input v-model="selectedCampaign.start_date" type="date" required>
          <label>End Date:</label>
          <input v-model="selectedCampaign.end_date" type="date">
          <label>Payment:</label>
          <input v-model="selectedCampaign.payment" type="text" required>
          <div class="modal-buttons">
            <button type="submit" class="btn btn-success">Create</button>
            <button @click="showCreateModal = false" class="btn btn-danger">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Campaign List -->
    <h3 style="color: lightseagreen; position: relative; left: 40px;">Your Campaigns</h3>
    <p style="color: lightseagreen; position: relative; left: 40px;">Here are the campaigns you have created. You can edit, delete, or toggle visibility of each campaign.</p>
    <div v-if="campaigns.length > 0" class="campaign-list">
      <ul>
        <li v-for="campaign in campaigns" :key="campaign.campaign_id" class="campaign-item">
          <span><h5>Campaign name:</h5> {{ campaign.campaign_name }}</span>
          <div class="campaign-actions">
            <button @click="editCampaignModal(campaign)" class="btn btn-info">Edit</button>
            <button :style="toggleVisibilityButtonStyle(campaign)" @click="toggleVisibility(campaign)" style="padding: 8px; margin-left: 10px; color: white; border: none; border-radius: 3px;">
              {{ campaign.is_active ? 'Public' : 'Private' }}
            </button>
            <button @click="deleteCampaign(campaign)" class="btn btn-danger">Delete</button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No campaigns found.</p>
    </div>
    
    <!-- Flagged Campaigns by admin -->
    <div v-if="flaggedCampaigns.length > 0" class="campaign-list">
      <h3>Flagged Campaigns</h3>
      <p class="alert alert-warning">These campaigns have been flagged by the admin for inappropriate content. Please review and take necessary action. Else it will be removed within 24 hours</p>
      <ul>
        <li v-for="campaign in flaggedCampaigns" :key="campaign.campaign_id" class="campaign-item">
          <span><h5>Campaign name:</h5> {{ campaign.campaign_name }}</span>
          <div class="campaign-actions">
            <button @click="editCampaignModal(campaign)" class="btn btn-info">Edit</button>
            <button :style="toggleVisibilityButtonStyle(campaign)" @click="toggleVisibility(campaign)" style="padding: 8px; margin-left: 10px; color: white; border: none; border-radius: 3px;">
              {{ campaign.is_active ? 'Public' : 'Private' }}
            </button>
            <button @click="deleteCampaign(campaign)" class="btn btn-danger">Delete</button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Edit Campaign Modal -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Edit Campaign</h3>
        <form @submit.prevent="updateCampaign">
          <label>Campaign Name:</label>
          <input v-model="selectedCampaign.campaign_name" type="text" required>
          <label>Ad Niche:</label>
          <select v-model="selectedCampaign.ad_niche" required>
            <option disabled value="">Select Niche</option>
            <option value="Fashion">Fashion</option>
            <option value="Beauty">Beauty</option>
            <option value="Fitness">Fitness</option>
            <option value="Food">Food</option>
            <option value="Travel">Travel</option>
            <option value="Gaming">Gaming</option>
            <option value="Technology">Technology</option>
            <option value="Lifestyle">Lifestyle</option>
            <option value="Education">Education</option>
            <option value="Health">Health</option>
          </select>
          <label>Ad Description:</label>
          <textarea v-model="selectedCampaign.ad_description" required></textarea>
          <label>Terms and Conditions:</label>
          <textarea v-model="selectedCampaign.terms_and_conditions" required></textarea>
          <label>Start Date:</label>
          <input v-model="selectedCampaign.start_date" type="date" required>
          <label>End Date:</label>
          <input v-model="selectedCampaign.end_date" type="date">
          <label>Payment:</label>
          <input v-model="selectedCampaign.payment" type="text" required>
          <div class="modal-buttons">
            <button type="submit" class="btn btn-success">Update</button>
            <button @click="showEditModal = false" class="btn btn-danger">Cancel</button>
          </div>
        </form>
      </div></div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['sponsorname'],
  data() {
    return {
      token: localStorage.getItem('access_token'),
      storedUsername: localStorage.getItem('username'),
      role: localStorage.getItem('role_id'),
      theme: localStorage.getItem('theme') || 'light',
      campaigns: [],
      flaggedCampaigns: [],
      showCreateModal: false,
      showEditModal: false,
      selectedCampaign: {
        campaign_id: null,
        campaign_name: '',
        ad_niche: '',
        ad_description: '',
        terms_and_conditions: '',
        start_date: '',
        end_date: '',
        payment: '',
        is_active: true,
      },
    };
  },
  created() {
    if (!this.token || this.role !== '3' || this.sponsorname !== this.storedUsername) {
      this.$router.push('/s/' + this.storedUsername + '/dashboard');
    } else {
      this.fetchCampaigns();
      this.fetchFlaggedCampaigns();
    }
  },
  methods: {
    async fetchCampaigns() {
      if (!this.sponsorname) {
        console.error('Sponsor name is not set');
        return;
      }
      try {
        const response = await fetch(`/api/s/${this.sponsorname}/campaigns`);
        if (response.ok) {
          this.campaigns = await response.json();
        } else {
          console.error('Error fetching campaigns:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching campaigns:', error);
      }
    },

    async fetchFlaggedCampaigns() {
      if (!this.sponsorname) {
        console.error('Sponsor name is not set');
        return;
      }
      try {
        const response = await fetch(`/api/s/${this.sponsorname}/campaigns?flagged=true`);
        if (response.ok) {
          this.flaggedCampaigns = await response.json();
        } else {
          console.error('Error fetching flagged campaigns:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching flagged campaigns:', error);
      }
    },

    async createCampaign() {
      try {
        const response = await fetch(`/api/s/${this.sponsorname}/campaigns`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.selectedCampaign),
        });
        if (response.ok) {
          this.showCreateModal = false;
          this.fetchCampaigns();
        } else {
          console.error('Error creating campaign:', response.statusText);
        }
      } catch (error) {
        console.error('Error creating campaign:', error);
      }
    },

    async updateCampaign() {
      try {
        const response = await fetch(`/api/s/${this.sponsorname}/campaigns`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.selectedCampaign),
        });
        if (response.ok) {
          this.showEditModal = false;
          this.fetchCampaigns();
        } else {
          console.error('Error updating campaign:', response.statusText);
        }
      } catch (error) {
        console.error('Error updating campaign:', error);
      }
    },

    async deleteCampaign(campaign) {
      try {
        const response = await fetch(`/api/s/${this.sponsorname}/campaigns`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ campaign_id: campaign.campaign_id }),
        });
        if (response.ok) {
          this.fetchCampaigns();
          this.$router.go();
        } else {
          console.error('Error deleting campaign:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting campaign:', error);
      }
    },

    async toggleVisibility(campaign) {
      try {
        const response = await fetch(`/api/s/${this.sponsorname}/campaigns`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            campaign_id: campaign.campaign_id,
            is_active: !campaign.is_active,
            is_private: !campaign.is_private,
          }),
        });
        if (response.ok) {
          this.fetchCampaigns();
        } else {
          console.error('Error toggling visibility:', response.statusText);
        }
      } catch (error) {
        console.error('Error toggling visibility:', error);
      }
    },

    editCampaignModal(campaign) {
      this.selectedCampaign = { ...campaign };
      this.showEditModal = true;
    },

    toggleVisibilityButtonStyle(campaign) {
      return {
        backgroundColor: campaign.is_active ? '#4CAF50' : '#f44336',
      };
    },

    logout() {
      localStorage.removeItem('sponsorname');
      this.$router.push('/');
    },
  },

  mounted() {
    this.fetchCampaigns();
    this.fetchFlaggedCampaigns();
  },
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
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  background-color: white;
  width: 80%;
  max-width: 600px;
  max-height: 70vh;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow-y: auto; 
  position: relative;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-content label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-content textarea {
  height: 100px;
  resize: vertical;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 10px 15px;
  border-radius: 5px;
  font-size: 14px;
  border: none;
  cursor: pointer;
}

.btn-success {
  background-color: #4CAF50;
  color: white;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}
.modal-overlay {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  background-color: white;
  width: 90%;
  max-width: 600px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-content label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-content textarea {
  height: 100px;
  resize: vertical;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 10px 15px;
  border-radius: 5px;
  font-size: 14px;
  border: none;
  cursor: pointer;
}

.btn-success {
  background-color: #4CAF50;
  color: white;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}
.container {
  min-width: 100vw;
  height: 100vh;
  background: transparent;
}

.navbar {
  margin-bottom: 20px;
}

.header {
  margin: 20px;
}

.header h2 {
  margin-bottom: 10px;
}

.header hr {
  border: 1px solid lightseagreen;
  width: 50%;
}

.btn {
  border-radius: 10px;
  font-size: 16px;
  padding: 10px 20px;
  margin-right: 10px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-success {
  background-color: #4CAF50;
  color: white;
}

.btn-info {
  background-color: #2196F3;
  color: white;
}

.btn-warning {
  background-color: #FFC107;
  color: white;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}

.modal-overlay {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  background-color: white;
  width: 50%;
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 5px;
}

.modal-buttons {
  margin-top: 20px;
}

.campaign-list {
  background: cornsilk;
  margin: 20px auto;
  border-radius: 10px;
  border: 1px solid black;
  padding: 15px;
  width: 80%;
}

.campaign-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.campaign-actions button {
  margin-left: 10px;
}
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

button {
  cursor: pointer;
}

.alert-warning {
  background-color: #ffc107;
  color: #212529;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 15px;
}
</style>