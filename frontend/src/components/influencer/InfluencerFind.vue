<template>
  <div class="app-container">
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

    <div class="container mt-4" style="position: relative; top: 50px">
        <!-- Filtering -->
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Search users..." v-model="searchTerm" @input="filterUsers">
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
                    UserHandle:  {{ user.userhandle || user.username }}
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

        <!-- Modal for Profile View -->
        <div class="modal" tabindex="-1" role="dialog" v-if="showModal" style="display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5);">
          <div class="modal-dialog" role="document" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 600px; width: 80%;">
            <div class="modal-content" style="width: 100%; max-height: 650px; overflow: hidden;">
              <div class="modal-header" style="padding: 15px; background-color: #f5f5f5; border-top-left-radius: 10px; border-top-right-radius: 10px;">
                <h5 class="modal-title">{{ modalTitle }}</h5>
                <button type="button" class="btn-close" @click="closeModal"></button>
              </div>
              <div class="modal-body" style="padding: 15px;">
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
                <!-- <button class="btn btn-success mt-3" style="width: 100%;" :disabled="isRequestDisabled">Send Request</button> -->
              </div>
              <div class="modal-footer" style="padding: 15px; background-color: #f5f5f5; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;">
                <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
              </div>
            </div>
          </div>
        </div>
      </div></div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['username'],
  data() {
    return {
      users: [],
      sponsors: [],
      filteredUsers: [],
      filteredSponsors: [],
      selectedProfile: null,
      showModal: false,
      searchTerm: '',
      modalTitle: '',
      isRequestDisabled: true,
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
      this.fetchUsersAndSponsors();
    }
  },
  methods: {
    fetchUsersAndSponsors() {
      axios.get(`/api/u/${this.username}/find`)
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
    filterUsers() {
      this.filteredUsers = this.users.filter(user =>
        user.userhandle ? user.userhandle.toLowerCase().includes(this.searchTerm.toLowerCase()) : user.username.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
      this.filteredSponsors = this.sponsors.filter(sponsor =>
        sponsor.companyName.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    },
    viewUserProfile(user) {
      this.selectedProfile = user;
      this.modalTitle = 'User Profile';
      this.isRequestDisabled = false; 
      this.showModal = true;
    },
    viewSponsorProfile(sponsor) {
      this.selectedProfile = sponsor;
      this.modalTitle = 'Sponsor Profile';
      this.isRequestDisabled = true; // disabling request button for sponsors
      this.showModal = true;
    },
    closeModal() {
      this.selectedProfile = null;
      this.showModal = false;
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
  padding-left: 0;
  padding-right: 0;
}

.container {
  margin-top: 56px;
  padding: 20px;
}

.search-filter-bar {
  display: flex;
  flex-direction: column;
}

.card {
  margin-bottom: 20px;
}

.modal-dialog {
  max-width: 90%;
}

@media (max-width: 768px) {
  .modal-dialog {
    max-width: 95%;
  }
}
</style>