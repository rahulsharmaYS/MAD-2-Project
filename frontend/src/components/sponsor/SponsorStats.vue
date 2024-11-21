<template>
  <div class="app-container" style="overflow-y: auto; color: lightblue; margin-bottom: 20px;">
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
    <div class="container" style="position: relative; top: 10px;">
      <h1 class="mt-4">Sponsor Stats</h1>
      <p class="lead">Here are some stats about your campaigns and budget.</p>
    </div>
    <div class="export-container">
      <button @click="exportCampaigns" class="btn btn-primary">Export Campaigns as CSV</button>
      <div v-if="exportStatus" class="alert alert-info mt-3">
        {{ exportStatus }}
      </div>
    <div class="stats-container" style='position: relative; left: -25px;'>
      <div v-if="expectedBudget !== null" class="stats-box">
        <h4>Total Expected Budget (Active Campaigns)</h4>
        <p>${{ (expectedBudget || 0).toFixed(2) }}</p>
      </div>
      <div v-if="totalCampaigns !== null" class="stats-box">
        <h4>Total Campaigns (Inactive)</h4>
        <p>{{ totalCampaigns || 0 }}</p>
      </div>
      <!-- <div v-if="totalActiveCampaigns !== null" class="stats-box">
        <h4>Total Active Campaigns</h4>
        <p>{{ totalActiveCampaigns || 0 }}</p>
      </div> -->
      <div v-if="campaignsAllottedToUsers !== null" class="stats-box">
        <h4>Campaigns Allotted to Users</h4>
        <p>{{ campaignsAllottedToUsers || 0 }}</p>
      </div>
      <div v-if="allottedBudget !== null" class="stats-box">
        <h4>Allotted Expected Budget (Total Campaigns active and public)</h4>
        <p>${{ (allottedBudget || 0).toFixed(2) }}</p>
      </div>
    </div>
    <div class="charts-container">
      <div class="chart-box">
        <h4>Total Expected Budget</h4>
        <canvas id="expectedBudgetChart"></canvas>
      </div>
      <div class="chart-box">
        <h4>Allotted Expected Budget</h4>
        <canvas id="allottedBudgetChart"></canvas>
      </div>
    </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  props: {
    sponsorname: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      token: localStorage.getItem('access_token'),
      storedUsername: localStorage.getItem('username'),
      role: localStorage.getItem('role_id'),
      expectedBudget: null,
      totalCampaigns: null,
      totalActiveCampaigns: null,
      campaignsAllottedToUsers: null,
      allottedBudget: null,
      exportStatus: null,
      exportTaskId: null,
      expectedBudgetChart: null,
      allottedBudgetChart: null,
    };
  },
  async mounted() {
    if (!this.token || this.role !== '3' || this.sponsorname !== this.storedUsername) {
      this.$router.push('/s/' + this.storedUsername + '/dashboard');
    } else {
      await this.fetchStats();
      this.renderCharts();
    }
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get(`/api/s/${this.sponsorname}/stats`, {
          headers: { Authorization: `Bearer ${this.token}` },
        });

        const stats = response.data;

        this.expectedBudget = stats.expected_budget || 0;
        this.totalCampaigns = stats.total_campaigns || 0;
        this.totalActiveCampaigns = stats.total_active_campaigns || 0;
        this.campaignsAllottedToUsers = stats.campaigns_allotted_to_users || 0;
        this.allottedBudget = stats.allotted_budget || 0;
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    },
    renderCharts() {
      const expectedBudgetCtx = document.getElementById('expectedBudgetChart').getContext('2d');
      if (this.expectedBudgetChart) {
        this.expectedBudgetChart.destroy();
      }
      this.expectedBudgetChart = new Chart(expectedBudgetCtx, {
        type: 'pie',
        data: {
          labels: ['Expected Budget'],
          datasets: [{
            data: [this.expectedBudget],
            backgroundColor: ['rgba(75, 192, 192, 0.2)'],
            borderColor: ['rgba(75, 192, 192, 1)'],
            borderWidth: 1,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });

      const allottedBudgetCtx = document.getElementById('allottedBudgetChart').getContext('2d');
      if (this.allottedBudgetChart) {
        this.allottedBudgetChart.destroy();
      }
      this.allottedBudgetChart = new Chart(allottedBudgetCtx, {
        type: 'pie',
        data: {
          labels: ['Allotted Budget'],
          datasets: [{
            data: [this.allottedBudget],
            backgroundColor: ['rgba(153, 102, 255, 0.2)'],
            borderColor: ['rgba(153, 102, 255, 1)'],
            borderWidth: 1,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    },
//     async exportCampaigns() {
//   try {
//     const response = await axios.post(`/api/s/${this.sponsorname}/stats`, null, {
//       action: 'export',
//       headers: {
//         Authorization: `Bearer ${this.token}`,
//       }
//     });

//     if (response.status === 200) {
//       this.exportStatus = 'Export initiated. You will receive an email with the CSV file soon.';
//     } else {
//       this.exportStatus = 'Export failed. Please try again later.';
//     }
//   } catch (error) {
//     console.error('Error exporting campaigns:', error);
//     this.exportStatus = 'Error exporting campaigns. Please try again later.';
//   }
// }
async exportCampaigns() {
  try {
    const response = await axios.post(`/api/s/${this.sponsorname}/stats`, 
      { action: 'export' }, 
      {
        headers: {
          Authorization: `Bearer ${this.token}`,
          'Content-Type': 'application/json', 
        }
      }
    );

    if (response.status === 202) { 
      this.exportStatus = 'Export initiated. You will receive an email with the CSV file soon.';
    } else {
      this.exportStatus = 'Export failed. Please try again later.';
    }
  } catch (error) {
    console.error('Error exporting campaigns:', error);
    this.exportStatus = 'Error exporting campaigns. Please try again later.';
  }
}


,
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('role_id');
      localStorage.removeItem('sponsorname');
      this.$router.push('/login');
    },
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

.navbar-brand {
  color: #ffffff;
}

.navbar-nav .nav-link {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.logout-link {
  cursor: pointer;
}

.container {
  color: lightseagreen;
}

.stats-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  height:fit-content;
  flex: 1;
  overflow-y: hidden;
  overflow-x: auto;
}

.stats-box {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stats-box h4 {
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333333;
}

.stats-box p {
  font-size: 1.5rem;
  font-weight: 500;
  color: #555555;
}

.charts-container {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.chart-box {
  flex: 1;
  min-width: 0;
  max-width: 100%;
  height: 40vh;
}

@media (max-width: 768px) {
  .chart-box {
    height: 300px;
  }

  .stats-box {
    padding: 15px;
  }

  .stats-box h4 {
    font-size: 1rem;
  }

  .stats-box p {
    font-size: 1.2rem;
  }
}

.export-container {
  margin-top: 20px;
}

.export-container .btn {
  font-size: 1rem;
}

.alert {
  font-size: 0.9rem;
}
</style>
