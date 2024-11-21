<template>
  <div class="app-container" style="overflow-x: hidden;">
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

    <div class="container mt-5 profile-container" style="position: relative; top: 50px;">
      <div class="card profile-card">
        <div class="card-body">
          <div class="profile-header d-flex align-items-center">
            <div class="profile-pic-container">
              <img :src="profilePicSrc" alt="Profile Picture" @click="triggerFileInput" class="profile-pic"/>
              <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" />
            </div>
            <div class="profile-info ms-4">
              <h5>Your Company Name</h5>
              <h3 v-if="!editing.companyName">{{ profileData.companyName }}</h3>
              <input v-else type="text" v-model="profileData.companyName" class="form-control">
              <button v-if="!editing.companyName" class="btn btn-sm btn-outline-primary ms-2" @click="editField('companyName')">Edit</button>
              <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('companyName')">Save</button>
              <button v-if="editing.companyName" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('companyName')">Cancel</button>
            </div>
          </div>
          <hr>
          <div class="profile-details mt-4">
            <h4>Contact Information</h4>
            <p>Email: 
              <span v-if="!editing.email">{{ profileData.email }}</span>
              <input v-else type="email" v-model="profileData.email" class="form-control">
              <button v-if="!editing.email" class="btn btn-sm btn-outline-primary ms-2" @click="editField('email')">Edit</button>
              <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('email')">Save</button>
              <button v-if="editing.email" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('email')">Cancel</button>
            </p>
            <p>Contact Number: 
              <span v-if="!editing.contactNumber">{{ profileData.contactNumber }}</span>
              <input v-else type="tel" v-model="profileData.contactNumber" class="form-control">
              <button v-if="!editing.contactNumber" class="btn btn-sm btn-outline-primary ms-2" @click="editField('contactNumber')">Edit</button>
              <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('contactNumber')">Save</button>
              <button v-if="editing.contactNumber" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('contactNumber')">Cancel</button>
            </p>
            <p>Company Website: 
              <span v-if="!editing.companyWebsite">{{ profileData.companyWebsite }}</span>
              <input v-else type="text" v-model="profileData.companyWebsite" class="form-control">
              <button v-if="!editing.companyWebsite" class="btn btn-sm btn-outline-primary ms-2" @click="editField('companyWebsite')">Edit</button>
              <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('companyWebsite')">Save</button>
              <button v-if="editing.companyWebsite" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('companyWebsite')">Cancel</button>
            </p>
            <p>Industry: 
              <span v-if="!editing.industry">{{ profileData.industry }}</span>
              <input v-else type="text" v-model="profileData.industry" class="form-control">
              <button v-if="!editing.industry" class="btn btn-sm btn-outline-primary ms-2" @click="editField('industry')">Edit</button>
              <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('industry')">Save</button>
              <button v-if="editing.industry" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('industry')">Cancel</button>
            </p>
            <small style="color:teal;"> Choose from [Fashion, Beauty, Fitness, Food, Travel, Gaming, Technology, Lifestyle, Education, Health] Industry type only!</small>
            <p style="color:red;"> Editing other industry type will lead to non visibility from the app.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      token: localStorage.getItem('access_token'),
      storedUsername: localStorage.getItem('username'),
      role: localStorage.getItem('role_id'),
      theme: localStorage.getItem('theme') || 'light',
      profileData: {
        companyName: '',
        companyWebsite: '',
        email: '',
        contactNumber: '',
        industry: '',
        profilePicUrl: ''
      },
      editing: {
        companyName: false,
        companyWebsite: false,
        email: false,
        contactNumber: false,
        industry: false
      },
      selectedFile: null,
      sponsorname: this.$route.params.sponsorname
    };
  },
  created(){
    if (!this.token || this.role !== '3' || this.sponsorname !== this.storedUsername) {
      this.$router.push('/s/'+this.storedUsername+'/dashboard');
    } else {
      this.fetchProfileData();
    }
  },
  computed: {
    profilePicSrc() {
      if (this.profileData.profilePicUrl) {
        return `data:image/jpeg;base64,${this.profileData.profilePicUrl}`;
      }
      return 'https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png';
    }
  },
  methods: {
    fetchProfileData() {
      axios.get(`http://localhost:8080/api/s/${this.sponsorname}/profile`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      }).then(response => {
        this.profileData = response.data;
      }).catch(error => {
        console.error('Error fetching profile data:', error);
      });
    },
    editField(field) {
      this.editing[field] = true;
    },
    cancelEdit(field) {
      this.editing[field] = false;
    },
    saveField(field) {
      axios.put(`http://localhost:8080/api/s/${this.sponsorname}/profile`, this.profileData, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      }).then(response => {
        this.profileData = response.data;
        this.editing[field] = false;
      }).catch(error => {
        console.error('Error updating profile data:', error);
      });
    },
    uploadProfilePicture() {
      if (this.selectedFile) {
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64String = reader.result.split(',')[1];
          this.profileData.profilePicUrl = base64String; 
          this.saveField('profilePicUrl');
        };
        reader.readAsDataURL(this.selectedFile);
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.uploadProfilePicture();
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/sponsorlogin');
    }
  },
  mounted() {
    this.fetchProfileData();
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