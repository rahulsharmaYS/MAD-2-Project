<template>
  <div class="app-container" style="overflow-x: hidden; color: aliceblue; overflow-y: auto;">
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

    <div class="container mt-5 profile-container">
      <div class="card profile-card">
        <div class="card-body">
          <div class="profile-header d-flex align-items-center">
            <div class="profile-pic-container">
              <img :src="profilePicSrc" alt="Profile Picture" @click="triggerFileInput" class="profile-pic"/>
              <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" />
            </div>
            <div class="profile-info ms-4">
              <h5>Your User Handle</h5>
              <h3 id="profile-name" v-if="!editing.name">{{ profileData.userhandle }}</h3>
              <input v-else type="text" v-model="profileData.userhandle" class="form-control">
              <button v-if="!editing.name" class="btn btn-sm btn-outline-primary ms-2" @click="editField('name')">Edit</button>
              <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('name')">Save</button>
              <button v-if="editing.name" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('name')">Cancel</button>
              <div class="ratings mt-2" id="rating-container">
                <span class="fas fa-star"></span>
                <span class="fas fa-star"></span>
                <span class="fas fa-star"></span>
                <span class="fas fa-star"></span>
                <span class="fas fa-star-half-alt"></span>
                <span>(4.5)</span>
              </div>
              <p class="mt-2"><strong>Bio: </strong> 
                <span v-if="!editing.bio">{{ profileData.bio }}</span>
                <textarea v-else v-model="profileData.bio" class="form-control"></textarea>
                <button v-if="!editing.bio" class="btn btn-sm btn-outline-primary ms-2" @click="editField('bio')">Edit</button>
                <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('bio')">Save</button>
                <button v-if="editing.bio" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('bio')">Cancel</button>
              </p>
              <p><strong>Reach:</strong> {{ profileData.reach }}</p>
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
            <p>Phone: 
              <span v-if="!editing.phone">{{ profileData.phone }}</span>
              <input v-else type="tel" v-model="profileData.phone" class="form-control">
              <button v-if="!editing.phone" class="btn btn-sm btn-outline-primary ms-2" @click="editField('phone')">Edit</button>
              <button v-else class="btn btn-sm btn-outline-success ms-2" @click="saveField('phone')">Save</button>
              <button v-if="editing.phone" class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('phone')">Cancel</button>
            </p>
            <h4 class="mt-4">Social Media Handles</h4>
            <div v-if="!editing.socialMedia">
              <p>Instagram: 
                <a v-if="profileData.socialMedia && isValidUrl(profileData.socialMedia.instagram)" :href="profileData.socialMedia.instagram" target="_blank">
                  {{ profileData.socialMedia.instagram || 'Not provided' }}
                </a>
                <span v-else>Not provided</span>
              </p>
              <p>YouTube: 
                <a v-if="profileData.socialMedia && isValidUrl(profileData.socialMedia.youtube)" :href="profileData.socialMedia.youtube" target="_blank">
                  {{ profileData.socialMedia.youtube || 'Not provided' }}
                </a>
                <span v-else>Not provided</span>
              </p>
              <p>X: 
                <a v-if="profileData.socialMedia && isValidUrl(profileData.socialMedia.twitter)" :href="profileData.socialMedia.twitter" target="_blank">
                  {{ profileData.socialMedia.twitter || 'Not provided' }}
                </a>
                <span v-else>Not provided</span>
              </p>
              <button class="btn btn-sm btn-outline-primary" @click="editField('socialMedia')">Edit</button>
            </div>
            <div v-else>
              <div class="mb-3">
                <label for="instagram">Instagram:</label>
                <input type="text" id="instagram" v-model="newSocialMedia.instagram" class="form-control">
              </div>
              <div class="mb-3">
                <label for="youtube">YouTube:</label>
                <input type="text" id="youtube" v-model="newSocialMedia.youtube" class="form-control">
              </div>
              <div class="mb-3">
                <label for="twitter">Twitter:</label>
                <input type="text" id="twitter" v-model="newSocialMedia.twitter" class="form-control">
              </div>
              <button class="btn btn-sm btn-outline-success" @click="saveField('socialMedia')">Save</button>
              <button class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('socialMedia')">Cancel</button>
            </div>

            <h4 class="mt-4">Niche</h4>
            <!-- <small>Choose from [Fashion, Beauty, Fitness, Food, Travel, Gaming, Technology, Lifestyle, Education, Health] only! <small style="color: red;">Editing wrong niche will not let the sponsor find you!</small></small> -->
            <div v-if="!editing.niche">
              <p>Your Niche: {{ profileData.niche }}</p>
              <button class="btn btn-sm btn-outline-primary" @click="editField('niche')">Edit</button>
            </div>
            <div v-else>
              <div class="mb-3">
                <label for="niche">Niche:</label>
                <select id="niche" v-model="profileData.niche" class="form-control">
                  <option v-for="option in nicheOptions" :key="option" :value="option">
                    {{ option }}
                  </option>
                </select>
              </div>
              <button class="btn btn-sm btn-outline-success" @click="saveField('niche')">Save</button>
              <button class="btn btn-sm btn-outline-secondary ms-2" @click="cancelEdit('niche')">Cancel</button>
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
  data() {
    return {
      profileData: {
        userhandle: '',
        bio: '',
        email: '',
        phone: '',
        socialMedia: {
          instagram: '',
          youtube: '',
          twitter: ''
        },
        niche: '',
        profilePicUrl: '',
        reach: ''
      },
      editing: {
        name: false,
        bio: false,
        email: false,
        phone: false,
        socialMedia: false,
        niche: false,
        reach: false
      },
      selectedFile: null,
      newSocialMedia: {
        instagram: '',
        youtube: '',
        twitter: ''
      },
      nicheOptions: ['Fashion', 'Beauty', 'Fitness', 'Food', 'Travel', 'Gaming', 'Technology', 'Lifestyle', 'Education', 'Health'],
      username: this.$route.params.username,
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
      this.fetchProfileData();
    }
  },
  computed: {
    profilePicSrc() {
      return this.profileData.profilePicUrl
        ? `data:image/png;base64,${this.profileData.profilePicUrl}`
        : 'https://via.placeholder.com/150?text=User+Icon';
    }
  },
  methods: {
    fetchProfileData() {
      axios.get(`http://localhost:8080/api/u/${this.username}/profile`, {
        headers: {
          Authorization: `Bearer ${this.access_token}`
        }
      }).then(response => {
        this.profileData = response.data;
        this.newSocialMedia = { ...this.profileData.socialMedia };
      }).catch(error => {
        console.error('Error fetching profile data:', error);
      });
    },
    editField(field) {
      this.editing[field] = true;
      if (field === 'socialMedia') {
        this.newSocialMedia = { ...this.profileData.socialMedia };
      }
    },
    cancelEdit(field) {
      this.editing[field] = false;
      if (field === 'socialMedia') {
        this.newSocialMedia = { ...this.profileData.socialMedia };
      }
    },
    saveField(field) {
      if (field === 'socialMedia') {
        this.profileData.socialMedia = this.formatSocialMediaUrls(this.newSocialMedia);
      }
      axios.put(`http://localhost:8080/api/u/${this.username}/profile`, this.profileData, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.access_token}`
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
      localStorage.removeItem('role_id');
      localStorage.removeItem('username');
      this.$router.push('/login');
    },
    isValidUrl(url) {
      try {
        new URL(url);
        return true;
      } catch (_) {
        return false;
      }
    },
    formatSocialMediaUrls(socialMedia) {
      const formattedSocialMedia = { ...socialMedia };
      const formatUrl = (url) => {
        if (!url) return url;
        if (!/^https?:\/\//i.test(url)) {
          return `https://${url}`;
        }
        return url;
      };

      formattedSocialMedia.instagram = formatUrl(formattedSocialMedia.instagram);
      formattedSocialMedia.youtube = formatUrl(formattedSocialMedia.youtube);
      formattedSocialMedia.twitter = formatUrl(formattedSocialMedia.twitter);

      return formattedSocialMedia;
    }
  },
  mounted() {
    this.fetchProfileData();
  }
};
</script>

<style scoped>
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
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
}

.profile-card {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.profile-pic-container {
  position: relative;
}

.profile-pic {
  width: 150px;
  height: 150px;
  border-radius: 10%;
  object-fit: cover;
  cursor: pointer;
}

.profile-info {
  margin-left: 20px;
}

.profile-info button {
  margin-left: 10px;
}

.ratings .fas {
  color: #FFD700;
}
</style>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';

.app-container {
  height: 100vh;
  width: 100vw;
  min-width: 100vw;
  position: relative;
  left: 25px;
  overflow-x: hidden;
}

.profile-card {
  max-width: 100%;
  margin: 0 auto;
}

.profile-pic-container {
  position: relative;
}

.profile-pic {
  width: 150px;
  height: 150px;
}

.profile-info {
  position: relative;
}

.ratings {
  display: flex;
  align-items: center;
}

.ratings .fas {
  color: gold;
}

.profile-details {
  margin-top: 1rem;
}
</style>