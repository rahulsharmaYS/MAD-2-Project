<template>
  <div class="app-container" style="overflow-y: auto;">
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
      <h1 class="display-4" style="color: lightseagreen;">Admin Dashboard - Statistics</h1>
      <button @click="exportData" class="btn btn-primary">Download Current Data</button>
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Total Influencers</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ totalUsers }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Total Sponsors</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ totalSponsors }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Total Campaigns</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ totalCampaigns }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Total Active Campaigns</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ activeCampaigns }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Total Banned Influencers</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ banneduser }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Total Banned Sponsors</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ bannedsponsor }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Most Reached Influencer</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ topusername }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Most Earning Influencer</h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ topearningusername }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Average Influencer Earning </h5>
              <p class="card-text display-4" :style="{ color: '#007bff' }">{{ average_earning }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Users vs Sponsors (Pie Chart)</h5>
              <div class="chart-container">
                <canvas id="usersSponsorsPieChart"></canvas>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Niche Distribution (Pie Chart)</h5>
              <div class="chart-container">
                <canvas id="userNicheDistributionChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
              <h5 class="card-title">Sponsor Industry Distribution (Pie Chart)</h5>
              <div class="chart-container">
                <canvas id="sponsorIndustryDistributionChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: ['username'],
  data() {
    return {
      token: localStorage.getItem('token'),
      storedUsername: localStorage.getItem('username'),
      role: localStorage.getItem('role_id'),
      theme: localStorage.getItem('theme') || 'light',
      totalUsers: 0,
      totalSponsors: 0,
      totalCampaigns: 0,
      activeCampaigns: 0,
      userNicheDistribution: {},
      sponsorIndustryDistribution: {},
      banneduser: 0,
      bannedsponsor: 0,
      topusername: '',
      topearningusername: '',
      average_earning: 0
    };
  },
  created() {
    if (!this.token || !this.storedUsername || this.role !== '1') {
      this.$router.push('/a/'+this.storedUsername+'/stats');
    } else {
      this.fetchStats();
    }
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await fetch(`/api/a/${this.username}/stats`);
        if (!response.ok) {
          throw new Error('Failed to fetch statistics');
        }
        const data = await response.json();
        this.totalUsers = data.total_users || 0;
        this.totalSponsors = data.total_sponsors || 0;
        this.totalCampaigns = data.total_campaigns || 0;
        this.activeCampaigns = data.active_campaigns || 0;
        this.userNicheDistribution = data.user_niche_distribution || {};
        this.sponsorIndustryDistribution = data.sponsor_industry_distribution || {};
        this.banneduser = data.banned_users || 0;
        this.bannedsponsor = data.banned_sponsors || 0;
        this.topusername = data.topusername || '';
        this.topearningusername = data.topearningusername || '';
        this.average_earning = data.average_earning || 0;

        this.renderCharts();
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    },
    exportData(){
      const data = {
      totalUsers: this.totalUsers,
      totalSponsors: this.totalSponsors,
      totalCampaigns: this.totalCampaigns,
      activeCampaigns: this.activeCampaigns,
      banneduser: this.banneduser,
      bannedsponsor: this.bannedsponsor,
      topusername: this.topusername,
      topearningusername: this.topearningusername,
      average_earning: this.average_earning,
      userNicheDistribution: this.userNicheDistribution,
      sponsorIndustryDistribution: this.sponsorIndustryDistribution
    };

    let csvContent = "data:text/csv;charset=utf-8,";

    csvContent += "Metric,Value\n";
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'object') {
        csvContent += `${key},${JSON.stringify(value).replace(/,/g, ';')}\n`;
      } else {
        csvContent += `${key},${value}\n`;
      }
    }

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'sponsornetdata.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },
    renderCharts() {
      new Chart(document.getElementById('usersSponsorsPieChart'), {
        type: 'pie',
        data: {
          labels: ['Users', 'Sponsors'],
          datasets: [{
            data: [this.totalUsers, this.totalSponsors],
            backgroundColor: ['#007bff', '#28a745']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top'
            },
            tooltip: {
              callbacks: {
                label: (context) => `${context.label}: ${context.raw}`
              }
            }
          }
        }
      });

      new Chart(document.getElementById('userNicheDistributionChart'), {
        type: 'pie',
        data: {
          labels: Object.keys(this.userNicheDistribution),
          datasets: [{
            data: Object.values(this.userNicheDistribution),
            backgroundColor: Object.keys(this.userNicheDistribution).map((_, index) => `hsl(${index * 360 / Object.keys(this.userNicheDistribution).length}, 70%, 70%)`)
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top'
            },
            tooltip: {
              callbacks: {
                label: (context) => `${context.label}: ${context.raw}`
              }
            }
          }
        }
      });

      new Chart(document.getElementById('sponsorIndustryDistributionChart'), {
        type: 'pie',
        data: {
          labels: Object.keys(this.sponsorIndustryDistribution),
          datasets: [{
            data: Object.values(this.sponsorIndustryDistribution),
            backgroundColor: Object.keys(this.sponsorIndustryDistribution).map((_, index) => `hsl(${index * 360 / Object.keys(this.sponsorIndustryDistribution).length}, 70%, 70%)`)
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top'
            },
            tooltip: {
              callbacks: {
                label: (context) => `${context.label}: ${context.raw}`
              }
            }
          }
        }
      });
    },
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.admin-stats {
  font-family: 'Roboto', sans-serif;
  background-color: transparent;
  margin: 0;
  padding: 0;
  height: 100vh;
  overflow-x: hidden;
  /* overflow-y:auto; */
}

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

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-weight: bold;
  font-size: 1.2rem;
}

.card-text {
  font-size: 2.5rem;
  font-weight: bold;
  color: #007bff;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 300px;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>