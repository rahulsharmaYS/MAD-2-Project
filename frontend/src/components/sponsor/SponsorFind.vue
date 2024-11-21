<template>
  <div class="app-container" style="color: lightseagreen;">
    <div class='sponsordashboard' style="height:100vh; width:100vw;">
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

      <div class="container mt-4" style="position: relative; top: 100px;">
        <!-- Filtering -->
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Search influencers by their niche or userhandle or minimum reach and sponsors by company..." v-model="searchTerm" @input="onSearchInputChange">
        </div>

        <!-- Tab System -->
        <ul class="nav nav-tabs" id="myTab" role="tablist">
          <li class="nav-item" role="presentation">
            <a class="nav-link active" id="users-tab" data-bs-toggle="tab" href="#users" role="tab" aria-controls="users" aria-selected="true">Influencers</a>
          </li>
          <li class="nav-item" role="presentation">
            <a class="nav-link" id="sponsors-tab" data-bs-toggle="tab" href="#sponsors" role="tab" aria-controls="sponsors" aria-selected="false">Sponsors</a>
          </li>
        </ul>

        <!-- Content -->
        <div class="tab-content mt-3" id="myTabContent">
          <!-- Influencers -->
          <div class="tab-pane fade show active" id="users" role="tabpanel" aria-labelledby="users-tab">
            <hr style="border: 1px solid black; width:50%;">
            <div v-if="filteredUsers.length === 0">
              <p>No users found.</p>
            </div>
            <ul class="list-group">
              <li v-for="user in filteredUsers" :key="user.id" class="list-group-item d-flex justify-content-between align-items-center">
                <img :src="user.profilePicUrl" alt="Profile Picture" style="width: 40px; height: 40px; border-radius: 20%;">
                UserHandle: {{ user.userhandle || user.username }}
                <button class="btn btn-sm btn-outline-primary ms-2" @click="viewUserProfile(user)">View Profile</button>
              </li>
            </ul>
          </div>

          <!-- Sponsors -->
          <div class="tab-pane fade" id="sponsors" role="tabpanel" aria-labelledby="sponsors-tab">
            <hr style="border: 1px solid black; width:50%;">
            <div v-if="filteredSponsors.length === 0">
              <p>No sponsors found.</p>
            </div>
            <ul class="list-group">
              <li v-for="sponsor in filteredSponsors" :key="sponsor.sponsor_id" class="list-group-item d-flex justify-content-between align-items-center">
                <img :src="sponsor.profilePicUrl" alt="Profile Picture" style="width: 40px; height: 40px; border-radius: 20%;">
                Company: {{ sponsor.companyName }}
                <button class="btn btn-sm btn-outline-primary ms-2" @click="viewSponsorProfile(sponsor)">View Profile</button>
              </li>
            </ul>
          </div>
        </div>

        <div class="modal" tabindex="-1" role="dialog" v-if="showModal" style="display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; background-color: rgba(0, 0, 0, 0.5);">
          <div class="modal-dialog" role="document" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 600px; width: 80%; height: 90vh;">
            <div class="modal-content" style="height: 100%; display: flex; flex-direction: column;">
        <div class="modal-header" style="padding: 15px; background-color: #f5f5f5; border-top-left-radius: 10px; border-top-right-radius: 10px;">
        <h5 class="modal-title">{{ modalTitle }}</h5>
        <button type="button" class="btn-close" @click="closeModal"></button>
      </div>
      <div class="modal-body" style="padding: 15px; overflow-y: auto; flex: 1;">
        <img :src="selectedProfile.profilePicUrl" alt="Profile Picture" style="width: 100px; height: 100px; display: block; margin: 0 auto; border-radius: 15%;">
        <h4>{{ selectedProfile.username || selectedProfile.companyName }}</h4>
        <p>Email: {{ selectedProfile.email }}</p>
        <p v-if="selectedProfile.phone">Phone: {{ selectedProfile.phone }}</p>
        <p v-if="selectedProfile.socialMedia && selectedProfile.socialMedia.instagram">
          Instagram: <a :href="selectedProfile.socialMedia.instagram" target="_blank">{{ selectedProfile.socialMedia.instagram }}</a>
        </p>
        <p v-if="selectedProfile.socialMedia && selectedProfile.socialMedia.youtube">
          YouTube: <a :href="selectedProfile.socialMedia.youtube" target="_blank">{{ selectedProfile.socialMedia.youtube }}</a>
        </p>
        <p v-if="selectedProfile.socialMedia && selectedProfile.socialMedia.twitter">
          Twitter: <a :href="selectedProfile.socialMedia.twitter" target="_blank">{{ selectedProfile.socialMedia.twitter }}</a>
        </p>
        <p v-if="selectedProfile.companyWebsite">
          Website: <a :href="selectedProfile.companyWebsite" target="_blank">{{ selectedProfile.companyWebsite }}</a>
        </p>
        <p v-if="selectedProfile.niche">
          Niche: {{ selectedProfile.niche }}
        </p>
        <p v-if="selectedProfile.industry">
          Industry: {{ selectedProfile.industry }}
        </p>
        <p v-if="selectedProfile.reach">
          Reach: {{ selectedProfile.reach }}
        </p>

        <!-- Campaign Selection and Request Form -->
        <div v-if="selectedProfile.username" class="mt-3">
          <label for="campaignSelect">Select Campaign:</label>
          <select id="campaignSelect" class="form-select" v-model="selectedCampaign" @change="fetchCampaignDetails">
            <option v-for="campaign in availableCampaigns" :key="campaign.campaign_id" :value="campaign.campaign_id">
              {{ campaign.campaign_name }}
            </option>
          </select>

          <div v-if="campaignDetails">
            <h5 class="mt-3">Campaign Details</h5>
            <p><strong>Ad Niche:</strong> {{ campaignDetails.ad_title }}</p>
            <p><strong>Description:</strong> {{ campaignDetails.ad_description }}</p>
            <p><strong>Terms:</strong> {{ campaignDetails.terms_and_conditions }}</p>
            <p><strong>Payment:</strong> {{ campaignDetails.payment }}</p>
            <button class="btn btn-success mt-3" @click="sendRequest">Send Request</button>
          </div>
        </div>
      </div>
      <div class="modal-footer" style="padding: 15px; background-color: #f5f5f5; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;">
        <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
      </div>
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
  props: ['sponsorname'],
  data() {
    return {
      token: localStorage.getItem('access_token'),
      storedUsername: localStorage.getItem('username'),
      role: localStorage.getItem('role_id'),
      theme: localStorage.getItem('theme') || 'light',
      users: [],
      sponsors: [],
      filteredUsers: [],
      filteredSponsors: [],
      selectedProfile: {},
      showModal: false,
      modalTitle: '',
      availableCampaigns: [],
      selectedCampaign: null,
      campaignDetails: null,
      searchTerm: '',
      isRequestDisabled: true
    };
  },
  created() {
    if (!this.token || this.role !== '3' || this.sponsorname !== this.storedUsername) {
      this.$router.push('/s/' + this.storedUsername + '/dashboard');
    } else {
      this.fetchUsersAndSponsors();
    }
    this.debouncedFilterResults = this.debounce(this.filterResults.bind(this), 500);

  },
  methods: {
    fetchUsersAndSponsors() {
      axios.get(`/api/s/${this.sponsorname}/find`)
        .then(response => {
          this.users = response.data.users;
          
          this.sponsors = response.data.sponsors;
          this.filteredUsers = this.users;
          this.filteredSponsors = this.sponsors;

        })
        .catch(error => {
          console.error('Error fetching users and sponsors:', error);
        });
    },
    // filterResults() {

    //   const parsedTerm = parseInt(this.searchTerm);
    //   this.filteredUsers = this.users.filter(user =>
    //     (user.userhandle ? user.userhandle.toLowerCase().includes(this.searchTerm.toLowerCase()) : user.username.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
    //     (user.niche && user.niche.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
    //     // all users with reach greater than or equal to the search term
    //     (!isNaN(parsedTerm) && user.reach >= parsedTerm)
        
    //     );
    //     console.log('Filtered Users:', this.filteredUsers);
    //   this.filteredSponsors = this.sponsors.filter(sponsor =>
    //     sponsor.companyName.toLowerCase().includes(this.searchTerm.toLowerCase())
    //   );
    // },

     debounce(fn, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
},
filterResults() {
  const parsedTerm = parseInt(this.searchTerm);
  this.filteredUsers = this.users.filter(user =>
    (user.userhandle ? user.userhandle.toLowerCase().includes(this.searchTerm.toLowerCase()) : user.username.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
    (user.niche && user.niche.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
    (!isNaN(parsedTerm) && user.reach >= parsedTerm)
  );
  this.filteredSponsors = this.sponsors.filter(sponsor =>
    sponsor.companyName.toLowerCase().includes(this.searchTerm.toLowerCase())
  );
},

// this.debouncedFilterResults = debounce(this.filterResults.bind(this), 500);

onSearchInputChange(event) {
  this.searchTerm = event.target.value;
  this.debouncedFilterResults();
},

    viewUserProfile(user) {
      this.selectedProfile = user;
      console.log('Selected Profile:', this.selectedProfile.reach);
      this.modalTitle = 'User Profile';
      this.isRequestDisabled = false;
      this.fetchCampaigns(user.username);
      this.showModal = true;
    },
    viewSponsorProfile(sponsor) {
      this.selectedProfile = sponsor;
      this.modalTitle = 'Sponsor Profile';
      this.isRequestDisabled = true;
      this.showModal = true;
    },
    closeModal() {
      this.selectedProfile = null;
      this.showModal = false;
    },
    async fetchCampaigns(username) {
      try {
        const response = await axios.get(`/api/s/${this.sponsorname}/find`);
        this.availableCampaigns = response.data.campaigns || [];
        console.log(username);
      } catch (error) {
        console.error('Error fetching campaigns:', error);
      }
    },
    async fetchCampaignDetails() {
      if (!this.selectedCampaign) return;
      try {
        const response = await axios.get(`/api/s/${this.sponsorname}/find`);
        this.campaignDetails = response.data.campaigns.find(c => c.campaign_id === this.selectedCampaign) || null;
      } catch (error) {
        console.error('Error fetching campaign details:', error);
      }
    },
    async sendRequest() {
    try {
        const response = await axios.post(`/api/s/${this.sponsorname}/find`, {
            influencer: this.selectedProfile.username,
            campaign_id: this.selectedCampaign
        });
        console.log('Response data:', response.data);
        alert('Request sent successfully!');
        this.closeModal();
    } catch (error) {
        console.error('Error sending request:', error);
        alert('Failed to send request.');
    }
},
    logout() {
      localStorage.removeItem('access_token');
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
</style>