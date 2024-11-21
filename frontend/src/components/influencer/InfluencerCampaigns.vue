<template>
  <div class="app-container" >
    <!-- Navbar -->
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

    <div class="container mt-4" style="position: relative; top: 50px;">
      <h2 class="section-title">Find Ad Campaigns</h2>
      <hr class="section-divider">

      <!-- Search Bar -->
      <div class="search-bar mb-3">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="form-control" 
          placeholder="Search by campaign or sponsor name or ad niche..." 
          aria-label="Search campaigns"
        />
      </div>

      <!-- Campaign List -->
      <div v-if="filteredCampaigns.length" class="campaign-list" style="overflow-y: auto;">
        <ul class="list-group">
          <li v-for="campaign in filteredCampaigns" :key="campaign.campaign_id" class="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <strong>Ad Name:</strong> {{ campaign.campaign_name }}
            </div>
            <div>
              <strong>By:</strong> {{ campaign.sponsor.sponsor_name }}
              <button @click="viewSponsorProfile(campaign.sponsor)" class="btn btn-secondary ms-2">
                {{ campaign.sponsor.profilePicUrl ? 'View Sponsor Profile' : 'No Profile Picture' }}
              </button>
            </div>
            <div>
              <button @click="viewCampaignDetails(campaign)" class="btn btn-info me-2">View Details</button>
              <button @click="negotiatePrice(campaign)" class="btn btn-warning me-2">Negotiate Price</button>
              <button @click="sendRequest(campaign)" class="btn btn-primary">Send Request</button>
            </div>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No active campaigns available.</p>
      </div>

      <!-- Sponsor Profile Modal -->
      <div v-if="showSponsorModal" class="modal fade show d-block" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Sponsor Profile</h5>
              <button type="button" class="btn-close" @click="showSponsorModal = false" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p><strong>Sponsor Name:</strong> {{ selectedSponsor.sponsor_name }}</p>
              <p><strong>Email:</strong> {{ selectedSponsor.email }}</p>
              <p><strong>Industry:</strong> {{ selectedSponsor.industry }}</p>
              <p><strong>Company Name:</strong> {{ selectedSponsor.companyName }}</p>
              <p><strong>Company Website:</strong> <a :href="ensureHttpPrefix(selectedSponsor.companyWebsite)" target="_blank">{{ selectedSponsor.companyWebsite }}</a></p>
              <p><strong>Contact Number:</strong> {{ selectedSponsor.contactNumber }}</p>
              <img :src="selectedSponsor.profilePicUrl" alt="Profile Picture" class="profile-pic">
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showSponsorModal = false">Close</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Campaign Details Modal -->
      <div v-if="showDetailsModal" class="modal fade show d-block" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Ad Details</h5>
              <button type="button" class="btn-close" @click="showDetailsModal = false" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p><strong>Ad Name:</strong> {{ selectedCampaign.campaign_name }}</p>
              <p><strong>Ad Niche:</strong> {{ selectedCampaign.ad_title }}</p>
              <p><strong>Ad Description:</strong> {{ selectedCampaign.ad_description }}</p>
              <p><strong>Terms and Conditions:</strong> {{ selectedCampaign.terms_and_conditions }}</p>
              <p><strong>Start Date:</strong> {{ selectedCampaign.start_date }}</p>
              <p><strong>End Date:</strong> {{ selectedCampaign.end_date }}</p>
              <p><strong>Payment:</strong> {{ selectedCampaign.payment }}</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showDetailsModal = false">Close</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Negotiate Price Modal -->
      <div v-if="showNegotiateModal" class="modal fade show d-block" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Negotiate Price</h5>
              <button type="button" class="btn-close" @click="showNegotiateModal = false" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p>Current Payment: {{ selectedCampaign.payment }}</p>
              <form @submit.prevent="submitNegotiation">
                <div class="mb-3">
                  <label class="form-label">Proposed Price:</label>
                  <input v-model.number="negotiatedPrice" type="number" step="0.01" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success">Submit</button>
                <button type="button" class="btn btn-danger" @click="showNegotiateModal = false">Cancel</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['username'],
  data() {
    return {
      campaigns: [],
      searchQuery: '',
      showDetailsModal: false,
      showNegotiateModal: false,
      showSponsorModal: false,
      selectedCampaign: {},
      selectedSponsor: {},
      negotiatedPrice: null,
      access_token: localStorage.getItem('access_token'),
      role_id: localStorage.getItem('role_id'),
      storedusername: localStorage.getItem('username')
    };
  },
  created() {
    if (!this.access_token) {
      this.$router.push('/login');
    } else if (this.role_id !== '2' || this.storedusername !== this.username) {
      this.$router.push(`/u/dashboard/${this.storedusername}`);
    } else {
      this.fetchCampaigns();
    }
  },
  computed: {
    filteredCampaigns() {
      const query = this.searchQuery.toLowerCase();
      return this.campaigns.filter(campaign => {
        return (
          campaign.campaign_name.toLowerCase().includes(query) || 
          campaign.sponsor.sponsor_name.toLowerCase().includes(query) ||
          campaign.ad_title.toLowerCase().includes(query)
        );
      });
    }
  },
  methods: {
    async fetchCampaigns() {
      if (!this.username) {
        console.error('Username is not set');
        return;
      }

      try {
        const response = await this.$axios.get(`/api/u/${this.username}/findcampaigns`);
        if (response.status === 200) {
          this.campaigns = response.data.campaigns || [];
        } else {
          console.error(`Error fetching campaigns: ${response.status} ${response.statusText}`);
        }
      } catch (error) {
        console.error('Error fetching campaigns:', error.message);
      }
    },
    viewCampaignDetails(campaign) {
      this.selectedCampaign = { ...campaign };
      this.showDetailsModal = true;
    },
    negotiatePrice(campaign) {
      this.selectedCampaign = { ...campaign };
      this.showNegotiateModal = true;
    },
    async submitNegotiation() {
      const requestData = {
        campaign_id: this.selectedCampaign.campaign_id,
        influencer_id: this.username,
        proposed_price: this.negotiatedPrice
      };

      try {
        const response = await this.$axios.post(`/api/u/${this.username}/findcampaigns`, requestData);
        if (response.status === 200) {
          this.showNegotiateModal = false;
          this.negotiatedPrice = null;
          await this.fetchCampaigns(); 
        } else {
          console.error('Error negotiating price:', response.statusText);
        }
      } catch (error) {
        console.error('Error negotiating price:', error.message);
      }
    },
    async sendRequest(campaign) {
      this.selectedCampaign = { ...campaign };
      const requestData = {
        campaign_id: this.selectedCampaign.campaign_id,
        influencer_id: this.username,
      };

      try {
        const response = await this.$axios.post(`/api/u/${this.username}/findcampaigns`, requestData);
        if (response.status === 200) {
          alert('Request sent successfully!');
          await this.fetchCampaigns();
        } else {
          console.error('Error sending request:', response.statusText);
        }
      } catch (error) {
        console.error('Error sending request:', error.message);
      }
    },
    viewSponsorProfile(sponsor) {
      this.selectedSponsor = { ...sponsor };
      this.showSponsorModal = true;
    },
    ensureHttpPrefix(url) {
      if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
        return `http://${url}`;
      }
      return url;
    },
    logout() {
      this.$router.push('/login');
    }
  },
  mounted() {
    this.fetchCampaigns();
  }
}
</script>


<style scoped>


.app-container {
  height: 100vh;
  width: 100vw;
  color: lightseagreen;
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
.section-title {
  color: aliceblue;
}

.section-divider {
  width: 35%;
  color: aliceblue;
}

.logout-link {
  cursor: pointer;
}

.profile-pic {
  max-width: 100px;
  height: auto;
}
</style>

<style scoped>
.container {
  padding: 20px;
}
.campaign-list {
  margin: 20px 0;
}
.list-group-item {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  padding: 15px;
  margin-bottom: 10px;
}
.profile-pic {
  width: 100px;
  height: 100px;
  border-radius: 10%;
  display: block;
  margin: 10px auto;
}
.btn {
  margin: 0 5px;
}
.navbar {
  margin-bottom: 20px;
}
.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background: rgba(0, 0, 0, 0.5);
}
.modal.fade.show.d-block {
  display: block;
}
.modal-dialog {
  margin: 15px auto;
}
.modal-content {
  background: white;
  border-radius: 5px;
}
.close {
  font-size: 1.5rem;
  color: #000;
}
</style>