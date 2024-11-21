<template>
  <div class="app-container" style="overflow-y: auto; color: lightblue;">
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

    <div class="container-fluid mt-5 pt-5" style="position: relative; top: -50px; ">
      <h1 class="mt-4">Your Stats</h1>
      <div class="stats-container">
        <div class="stats-details">
          <h4>Total Actual Earnings: ${{ earnings.toFixed(2) }}</h4>
          <hr width="50%">
          <h4>Total Expected Earnings: ${{ expected_earnings.toFixed(2) }}</h4>
        </div>
        <hr width="50%">

        <h3>Your Campaigns</h3>
        <div class="campaigns-container">          
          <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-box">
            <strong>Campaign Name: {{ campaign.campaign_name }}</strong><br>
            <strong>Ad: </strong>{{ campaign.ad_title }}<br>
            <strong>Info: </strong>{{ campaign.ad_description }}<br>
            <strong>T&C: </strong>{{ campaign.terms_and_conditions }}
          </div>
        </div>
        <hr width="60%">
        <!--charts thinf -->
        <div class="charts-container" style="background-color: rgba(0, 0, 0, 0.5); padding: 20px; border-radius: 10px;">
            <div class="stats-chart" id="reachChartSection">
              <h3>Reach Overview</h3>
              <canvas id="reachChart"></canvas>
            </div>
            <div class="stats-chart" id="earningsChartSection">
              <h3>Earnings Overview</h3>
              <canvas id="earningsChart"></canvas>
            </div>
          </div>
    </div></div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  props: ['username'],
  data() {
    return {
      access_token: localStorage.getItem('access_token'),
      role_id: localStorage.getItem('role_id'),
      storedusername: localStorage.getItem('username'),
      reachData: {
        labels: ['Reach'],
        datasets: [{
          label: 'Reach',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          data: [],
        }],
      },
      earningsData: {
        labels: ['Actual Earnings', 'Expected Earnings'],
        datasets: [{
          label: 'Earnings',
          backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)'],
          borderColor: ['rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
          borderWidth: 1,
          data: [],
        }],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
      earnings: 0,
      expected_earnings: 0,
      campaigns: [],
      reachChart: null,
      earningsChart: null,
    };
  },
  created() {
    if (!this.access_token) {
      this.$router.push('/login');
    } else if (this.role_id !== '2' || this.storedusername !== this.username) {
      this.$router.push(`/u/dashboard/${this.storedusername}`);
    } else {
      this.$emit('authenticated', this.username);
    }
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get(`/api/u/${this.username}/stats`, {
          headers: { Authorization: `Bearer ${this.access_token}` },
        });
        console.log('API Response:', response.data);
        const stats = response.data;

        this.reachData.datasets[0].data = [stats.reach || 0];
        this.earningsData.datasets[0].data = [stats.earning || 0, stats.expectedearning || 0];
        this.earnings = stats.earning || 0;
        this.expected_earnings = stats.expectedearning || 0;
        this.campaigns = stats.campaigns || [];

        console.log('Updated Earnings:', this.earnings);
        console.log('Updated Campaigns:', this.campaigns);

        this.renderReachChart();
        this.renderEarningsChart();
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    },
    renderReachChart() {
      const ctx = document.getElementById('reachChart').getContext('2d');
      if (this.reachChart) {
        this.reachChart.destroy(); 
      }
      this.reachChart = new Chart(ctx, {
        type: 'bar', 
        data: this.reachData,
        options: this.chartOptions,
      });
    },
    renderEarningsChart() {
      const ctx = document.getElementById('earningsChart').getContext('2d');
      if (this.earningsChart) {
        this.earningsChart.destroy(); 
      }
      this.earningsChart = new Chart(ctx, {
        type: 'bar', // can use 'line', 'bar', etc.
        data: this.earningsData,
        options: this.chartOptions,
      });
    },
    logout() {
      console.log('Logout clicked');
      localStorage.removeItem('access_token');
      localStorage.removeItem('role_id');
      localStorage.removeItem('username');
      this.$router.push('/login');
    },
  },
};
</script>
<style>
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

.stats-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.stats-details {
  margin-bottom: 20px; 
}

.campaigns-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
  gap: 20px; 
  padding: 10px;
  height: 100%; 
}

.campaign-box {
  flex: 0 0 auto;
  width: 300px;
  box-sizing: border-box;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; 
}

.charts-container {
  display: flex;
  gap: 20px; 
  justify-content: space-between;
}

.stats-chart {
  width: 45vw; 
  height: 40vh;
}

@media (max-width: 768px) {
  .campaign-box {
    flex: 1 1 calc(50% - 20px);
  }

  .stats-chart {
    width: 100%;
    height: 300px;
  }
}

@media (max-width: 576px) {
  .campaign-box {
    flex: 1 1 100%;
  }

  .stats-chart {
    height: 250px; 
  }
}
</style>
<style>
.stats-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.stats-details {
  margin-bottom: 20px;
}
.campaigns-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto; 
  overflow-y: hidden; 
  gap: 20px;
  padding: 10px; 
  height: 100%; 
}

.campaign-box {
  flex: 0 0 auto; 
  width: 300px;
  box-sizing: border-box;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px; 
  background-color: #ffffff; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}
.chart-container {
  display: flex;
  justify-content: flex-start;
}

.stats-chart {
  width: 40vw;
  height: 40vh;
}

@media (max-width: 768px) {
  .campaign-box {
    flex: 1 1 calc(50% - 20px);
  }
}

@media (max-width: 576px) {
  .campaign-box {
    flex: 1 1 100%;
  }

  .stats-chart {
    width: 100%;
    height: 250px;
  }
}

</style>
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
