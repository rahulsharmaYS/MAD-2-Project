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
    <div class="container mt-4" style="position: relative; top: 50px;">
      <h1 class="display-4" style="color: lightseagreen;">Admin Dashboard - Applications</h1>
      <div v-if="applications.length === 0" class="alert alert-info mt-4">No applications found</div>
      <div v-else class="table-responsive">
        <table class="table table-striped mt-4">
          <thead>
            <tr>
              <th scope="col">Sponsor Name</th>
              <th scope="col">Email</th>
              <th scope="col">Industry</th>
              <th scope="col">Company Name</th>
              <th scope="col">Company Website</th>
              <th scope="col">Contact Number</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="application in applications" :key="application.id">
              <td>{{ application.sponsor_name }}</td>
              <td>{{ application.email }}</td>
              <td>{{ application.industry }}</td>
              <td>{{ application.companyName }}</td>
              <td>{{ application.companyWebsite }}</td>
              <td>{{ application.contactNumber }}</td>
              <td>
                <button class="btn btn-success btn-sm" @click="handleApplication(application.id, 'approve')">Approve</button>
                <button class="btn btn-danger btn-sm" @click="handleApplication(application.id, 'reject')">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['username'],
  data() {
    return {
      token: localStorage.getItem('access_token'),
      storedUsername: localStorage.getItem('username'),
      role: localStorage.getItem('role_id'),
      theme: localStorage.getItem('theme') || 'light',
      applications: []
    };
  },
  created() {
    if (!this.token || this.role !== '1' || this.storedUsername !== this.username) {
      this.$router.push('/a/'+this.storedUsername+'/applications');
      setTimeout(() => {
        window.location.reload();
      }, 100);
    } else {
      this.fetchApplications();
    }
  },
  // mounted() {
  //   this.fetchApplications();
  // },
  methods: {
    async fetchApplications() {
      try {
        const response = await fetch(`/api/a/${this.username}/applications`);
        if (!response.ok) {
          throw new Error('Failed to fetch applications');
        }
        this.applications = await response.json();
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    },
    async handleApplication(applicationId, action) {
      try {
        const response = await fetch(`/api/a/${this.username}/applications`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ application_id: applicationId, action: action })
        });
        if (!response.ok) {
          throw new Error(`Failed to ${action} application`);
        }
        const result = await response.json();
        console.log(result.message); 
        this.fetchApplications();
      } catch (error) {
        console.error(`Error ${action} application:`, error);
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
</style>