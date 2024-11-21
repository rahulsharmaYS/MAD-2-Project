<template>
  <div class="app-container">
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
    <div class="container mt-4" style="position: relative; top: 50px">
      <h3 class="display-4" style="color: lightseagreen;">Search Users around the world!</h3>
      <hr style="width: 70%;">
        <!-- Filtering -->
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Search influencers by username or userhandle & sponsors by company..." v-model="searchTerm" @input="filterUsers">
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

        <!-- Main Content -->
        <div class="tab-content mt-3" id="myTabContent">
          <!-- Influencers -->
          <div class="tab-pane fade show active" id="users" role="tabpanel" aria-labelledby="users-tab">
            <hr style="border: 1px solid black; width:50%;">
            <div v-if="filteredUsers.length === 0">
              <p>No influencers found.</p>
            </div>
            <ul class="list-group">
              <li v-for="user in filteredUsers" :key="user.id" class="list-group-item d-flex justify-content-between align-items-center">
                <img :src="user.profilePicUrl" alt="Profile Picture" style="width: 40px; height: 40px; border-radius: 20%;">
                <span><strong>Name:</strong> {{ user.username }}</span>
                <span><strong>UserHandle:</strong> {{ user.userhandle || user.username }}</span>
                <div>
                  <button class="btn btn-sm btn-outline-primary ms-2" @click="viewUserProfile(user)">View Profile</button>
                  <button class="btn btn-sm ms-2" :class="{'btn-danger': user.is_banned, 'btn-success': !user.is_banned}" @click="toggleBan(user, 'user')">
                    {{ user.is_banned ? 'Unban' : 'Ban' }}
                  </button>
                </div>
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
                <span><strong>Name:</strong> {{ sponsor.sponsor_name }}</span>
                <span><strong>Company:</strong> {{ sponsor.companyName }}</span>
                <div>
                  <button class="btn btn-sm btn-outline-primary ms-2" @click="viewSponsorProfile(sponsor)">View Profile</button>
                  <button class="btn btn-sm ms-2" :class="{'btn-danger': sponsor.is_banned, 'btn-success': !sponsor.is_banned}" @click="toggleBan(sponsor, 'sponsor')">
                    {{ sponsor.is_banned ? 'Unban' : 'Ban' }}
                  </button>
                </div>
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
      role: localStorage.getItem('role_id'),
      theme: localStorage.getItem('theme') || 'light',
      users: [],
      sponsors: [],
      filteredUsers: [],
      filteredSponsors: [],
      selectedProfile: null,
      showModal: false,
      searchTerm: '',
      modalTitle: '',
      isRequestDisabled: true
    };
  },
  created() {
    if (!this.token || this.role !== '1' || this.storedUsername !== this.username) {
      this.$router.push('/a/'+this.storedUsername+'/find');
      setTimeout(() => {
        window.location.reload();
      }, 100);
    } else {
      this.fetchUsersAndSponsors();
    }
  },
  methods: {
    fetchUsersAndSponsors() {
      axios.get(`/api/a/${this.username}/find`)
        .then(response => {
          this.users = response.data.users;
          this.sponsors = response.data.sponsors;
          this.filteredUsers = this.users;
          console.log('Users:', this.users);
          this.filteredSponsors = this.sponsors;
        })
        .catch(error => {
          console.error('Error fetching users and sponsors:', error);
        });
    },
    filterUsers() {
      this.filteredUsers = this.users.filter(user => {
        const searchTerm = this.searchTerm.toLowerCase();
        return (user.userhandle && user.userhandle.toLowerCase().includes(searchTerm)) ||
           (user.username && user.username.toLowerCase().includes(searchTerm));
      });
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
      this.isRequestDisabled = true;
      this.showModal = true;
    },
    closeModal() {
      this.selectedProfile = null;
      this.showModal = false;
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/login');
    },
    toggleBan(item, type) {
      axios.post(`/api/a/${this.username}/find`, {
        id: type === 'user' ? item.id : item.sponsor_id,
        type: type,
        action: item.is_banned ? 'unban' : 'ban'
      })
      .then(() => {
        if (type === 'user') {
          item.is_banned = !item.is_banned;
        } else {
          item.is_banned = !item.is_banned;
        }
      })
      .catch(error => {
        console.error('Error toggling ban status:', error);
      });
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