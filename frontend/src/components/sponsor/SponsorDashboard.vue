<template>
  <div class="app-container" style="color: lightseagreen; overflow-y: auto;">
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

      <div class="container mt-4" style="position: relative; top: 50px;">
        <h1>Welcome, {{ sponsorname }}!</h1>
        <hr style="border: 1px solid black; width:50%;">
        <div class="active-campaigns">
          <h2>Active Campaigns</h2>
          <div v-if="activeRequests.length === 0">No active campaigns. Go to Campaigns tab to create one!</div>
          <div v-else class="list-group" style="max-height: 300px; overflow-y: auto;">
            <div class="list-group-item" v-for="request in activeRequests" :key="request.campaign_req_id">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h5 style="color:mediumslateblue;">Campaign Name:</h5>{{ request.campaign_name }}
                  <h5 style="color:mediumslateblue;">Influencer:</h5> {{ request.user.userhandle }}
                  <h5 style="color:mediumslateblue;">Final Price</h5> {{ request.negotiated_price }}
                </div>
                <div>
                  <button class="btn btn-primary" @click="viewCampaign(request.campaign_req_id)">View</button>
                  <button class="btn btn-danger" @click="showCancelConfirmation(request)">Cancel</button>
                  <button class="btn btn-success" @click="showCompleteConfirmation(request)">Mark Complete</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="new-requests mt-4">
          <h2>New Requests</h2>
          <div v-if="newRequests.length === 0">No new requests.</div>
          <div v-else class="list-group" style="max-height: 300px; overflow-y: auto;">
          <div class="list-group-item" v-for="request in newRequests" :key="request.id">
          <div class="d-flex justify-content-between align-items-center">
          <div>
          <span><h5> Campaign Name: </h5>{{ request.campaign_name }} <h5>From:</h5> {{ request.user_id }}</span>
        </div>
        <div>
        <h5> Negotiated Price:  {{ request.negotiated_price }}</h5>
        <button class="btn btn-warning" @click="openRenegotiateModal(request)">Renegotiate</button>
        <button class="btn btn-primary" @click="viewRequest(request)">View</button>
        <button class="btn btn-success" @click="showAcceptConfirmation(request)">Accept</button>
        <button class="btn btn-danger" @click="showDeleteConfirmation(request)">Reject</button>
      </div>
    </div>
  </div>
</div>

        </div>         

        <div class="sent-requests mt-4">
          <h2>Sent Requests</h2>
          <div v-if="sentRequests.length === 0">No sent requests.</div>
          <div v-else class="list-group" style="max-height: 300px; overflow-y: auto;">
            <div class="list-group-item" v-for="request in sentRequests" :key="request.id">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <span><h5>Campaign Name:</h5> {{ request.campaign_name }} <h5>From:</h5> {{ request.user_id }}</span>
                </div>
                <div>
                  <h5>Negotiated Price: {{ request.negotiated_price }}</h5>
                  <button class="btn btn-primary" @click="viewRequest(request)">View</button>
                   <button class="btn btn-warning" @click="editSentRequest(request)">Edit</button>
                  <button class="btn btn-danger" @click="showDeleteConfirmation(request)">Cancel</button>
                </div>
              </div>
            </div>
            </div>
        </div>
      </div>


          <!-- Edit Request Modal -->
          <div v-if="showEditRequestModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeEditModal">&times;</span>
        <h3>Edit Request</h3>
        <form @submit.prevent="submitEditRequest">
          <div class="form-group">
            <label for="newNegotiatedPrice">Negotiated Price:</label>
            <input type="number" v-model="newNegotiatedPrice" class="form-control" id="newNegotiatedPrice" required>
          </div>
          <div class="form-group">
            <label for="newStartDate">Start Date:</label>
            <input type="date" v-model="newStartDate" class="form-control" id="newStartDate" required>
          </div>
          <div class="form-group">
            <label for="newEndDate">End Date:</label>
            <input type="date" v-model="newEndDate" class="form-control" id="newEndDate" required>
          </div>
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </form>
      </div>
    </div>

      <!-- Request Details Modal -->
      <div v-if="showRequestModal" class="modal fade show" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Request Details</h5>
              <button type="button" class="btn-close" @click="hideModal('RequestModal')" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedRequest">
                <h5>Campaign Name: {{ selectedRequest.campaign_name }}</h5>
                <p><strong>From User:</strong> {{ selectedRequest.user_id }}</p>
                <p><strong>Negotiated Price:</strong> {{ selectedRequest.negotiated_price }}</p>
                <p><strong>Request Date:</strong> {{ selectedRequest.start_date }}</p>
                <p><strong>Status:</strong> {{ selectedRequest.status }}</p>
                <p><strong>End Date:</strong> {{ selectedRequest.end_date }}</p>
                <p>Search User details in find page!</p>
              </div>
              <div v-else>No request selected</div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="hideModal('RequestModal')">Close</button>
            </div>
          </div>
        </div>
      </div>


  <!-- Campaign Details Modal -->
        <div v-if="showCampaignModal" class="modal fade show" tabindex="-1" role="dialog">
          <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Campaign Details</h5>
                <button type="button" class="btn-close" @click="hideModal('CampaignModal')" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <div v-if="selectedCampaign">
                  <h5>Campaign Name: {{ selectedCampaign.campaign_name }}</h5>
                  <p><strong>Influencer:</strong> {{ selectedCampaign.user.userhandle }}</p>
                  <p><strong>Ad Title:</strong> {{ selectedCampaign.ad_title }}</p>
                  <p><strong>Terms and Condition:</strong>{{ selectedCampaign.terms_and_conditions }}</p>
                  <p><strong>Description:</strong> {{ selectedCampaign.ad_description }}</p>
                  <p><strong>Start Date:</strong> {{ selectedCampaign.start_date }}</p>
                  <p><strong>Status:</strong> {{ selectedCampaign.status }}</p>
                </div>
                <div v-else>No campaign selected</div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="hideModal('CampaignModal')">Close</button>
              </div>
            </div>
          </div>
        </div>



      <!-- Confirmation Modal for Accepting Request -->
      <div v-if="showAcceptConfirmationModal" class="modal fade show" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Confirm Acceptance</h5>
              <button type="button" class="btn-close" @click="hideModal('AcceptConfirmationModal')" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p v-if="selectedRequest">Are you sure you want to accept the request for "{{ selectedRequest.campaign_name }}"?</p>
              <p v-else>No request selected</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="hideModal('AcceptConfirmationModal')">Cancel</button>
              <button type="button" class="btn btn-success" @click="confirmAcceptRequest">Accept</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Confirmation Modal for Deleting Request -->
      <div v-if="showDeleteConfirmationModal" class="modal fade show" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Confirm Deletion</h5>
              <button type="button" class="btn-close" @click="hideModal('DeleteConfirmationModal')" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p v-if="selectedRequest">Are you sure you want to delete the request for "{{ selectedRequest.campaign_name }}"?</p>
              <p v-else>No request selected</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="hideModal('DeleteConfirmationModal')">Cancel</button>
              <button type="button" class="btn btn-danger" @click="confirmDeleteRequest">Delete</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Confirmation Modal for Cancelling Campaign -->
      <div v-if="showCancelConfirmationModal" class="modal fade show" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Confirm Cancellation</h5>
              <button type="button" class="btn-close" @click="hideModal('CancelConfirmationModal')" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p v-if="selectedRequest">Are you sure you want to cancel the campaign for "{{ selectedRequest.campaign_name }}"? Cancelling a request once accepted will be counted and doing this multiple times may lead to a ban.</p>
              <p v-else>No request selected</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="hideModal('CancelConfirmationModal')">Cancel</button>
              <button type="button" class="btn btn-danger" @click="confirmCancelCampaign">Cancel Campaign</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showRenegotiateModal" class="modal fade show" tabindex="-1" role="dialog">
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Renegotiate Price</h5>
        <button type="button" class="btn-close" @click="hideModal('RenegotiateModal')" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p v-if="selectedRequest">Enter the new negotiated price for "{{ selectedRequest.campaign_name }}":</p>
        <input type="number" v-model="newNegotiatedPrice" class="form-control" placeholder="New Negotiated Price">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="hideModal('RenegotiateModal')">Cancel</button>
        <button type="button" class="btn btn-warning" @click="confirmRenegotiate">Renegotiate</button>
      </div>
    </div>
  </div>


</div>

      <!-- showcompleteconfirmation modal -->
      <div v-if="showCompleteConfirmationModal" class="modal fade show" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Confirm Completion</h5>
              <button type="button" class="btn-close" @click="hideModal('CompleteConfirmationModal')" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p v-if="selectedRequest">Are you sure you want to mark the campaign for "{{ selectedRequest.campaign_name }}" as complete?</p>
              <p v-else>No request selected</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="hideModal('CompleteConfirmationModal')">Cancel</button>
              <button type="button" class="btn btn-success" @click="showCompleteConfirmation(selectedRequest)">Mark Complete</button>
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
      activeRequests: [],
      newRequests: [],
      selectedCampaign: null,
      selectedRequest: null,
      showRequestModal: false,
      showCampaignModal: false,
      showAcceptConfirmationModal: false,
      showEditRequestModal: false,
      showDeleteConfirmationModal: false,
      showCancelConfirmationModal: false,
      showCompleteConfirmationModal: false,
      showRenegotiateModal: false,
      newNegotiatedPrice: null,
      newStartDate: null,
      newEndDate: null,
      sentRequests: []
    };
  },
  created() {
    if (!this.token || this.role !== '3' || this.sponsorname !== this.storedUsername) {
      this.$router.push('/sponsorlogin');
    } else {
      this.fetchData();
    }
  },
  methods: {
    async fetchData() {
  try {
    const response = await axios.get(`/api/s/${this.sponsorname}/dashboard`);
    console.log("Fetched data:", response.data);
    this.activeRequests = response.data.activeRequests;
    this.newRequests = response.data.newRequests;
    this.sentRequests = response.data.sentRequests;
  } catch (error) {
    console.error("There was an error fetching the data!", error);
  }
},
    viewCampaign(campaignId) {
      console.log("Attempting to view campaign with ID:", campaignId);
      const campaign = this.activeRequests.find(req => req.campaign_req_id === campaignId);
      
      if (campaign) {
        this.selectedCampaign = campaign;
        console.log("Selected campaign:", this.selectedCampaign);
        this.showCampaignModal = true;
      } else {
        console.error("Campaign not found with ID:", campaignId);
        this.selectedCampaign = null;
      }
    },
    viewRequest(request) {
  console.log("Viewing request:", request);
  this.selectedRequest = request;
  // console.log("Selected request set to:", this.selectedRequest);
  this.showRequestModal = true;
},
openRenegotiateModal(request) {
  console.log("Opening renegotiate modal for request:", request);
  this.selectedRequest = request;
  console.log("Selected request set to:", this.selectedRequest);
  this.showRenegotiateModal = true;
},
    editSentRequest(request) {
      console.log("Editing sent request:", request);
      this.selectedRequest = request;
      this.newNegotiatedPrice = request.negotiated_price;
      this.newStartDate = request.start_date;
      this.newEndDate = request.end_date;
      this.showEditRequestModal = true;

    },
    closeEditModal() {
      this.showEditRequestModal = false;
    },
    async submitEditRequest() {
      if (this.newNegotiatedPrice == null || this.newNegotiatedPrice <= 0) {
        console.error("Invalid price.");
        return;
      }

      if (!this.newStartDate || !this.newEndDate) {
        console.error("Start date and end date are required.");
        return;
      }

      try {
        const response = await axios.post(`/api/s/${this.sponsorname}/dashboard`, {
          action: 'renegotiate',
          request_id: this.selectedRequest.campaign_req_id,
          new_price: this.newNegotiatedPrice,
          new_start_date: this.newStartDate,
          new_end_date: this.newEndDate,
          user_id: this.selectedRequest.user_id
        });
        
        this.sentRequests = response.data.sentRequests;
        this.showEditRequestModal = false;
      } catch (error) {
        console.error("Error while updating the sent request:", error);
      }
    },

    showAcceptConfirmation(request) {
      console.log("Showing accept confirmation for request:", request);
      this.selectedRequest = request;
      this.showAcceptConfirmationModal = true;
    },
    confirmAcceptRequest() {
      console.log("Confirming acceptance for request ID:", this.selectedRequest?.id);
      axios.post(`/api/s/${this.sponsorname}/dashboard`, { action: 'accept', request_id: this.selectedRequest.campaign_req_id, user_id: this.selectedRequest.user_id})
        .then(response => {
          console.log("Accept request response:", response.data);
          this.activeRequests = response.data.activeRequests;
          this.newRequests = response.data.newRequests;
          this.hideModal('AcceptConfirmationModal');
        })
        .catch(error => {
          console.error("There was an error accepting the request!", error);
        });
    },
    confirmRenegotiate() {
  console.log("Attempting to confirm renegotiation...");
  console.log("Selected request ID:", this.selectedRequest?.campaign_req_id); 
  console.log("New negotiated price:", this.newNegotiatedPrice);
  if (this.selectedRequest?.campaign_req_id && this.newNegotiatedPrice != null) {
    axios.post(`/api/s/${this.sponsorname}/dashboard`, {
      action: 'renegotiate',
      request_id: this.selectedRequest.campaign_req_id,
      new_price: this.newNegotiatedPrice,
      user_id: this.selectedRequest.user_id
    })
    .then(response => {
      console.log("Renegotiate request response:", response.data);
      this.activeRequests = response.data.activeRequests;
      this.newRequests = response.data.newRequests;
      this.hideModal('RenegotiateModal');
    })
    .catch(error => {
      console.error("There was an error renegotiating the request!", error);
    });
  } else {
    console.error("Selected request ID or new price is missing.");
  }
},
    showDeleteConfirmation(request) {
      console.log("Showing delete confirmation for request:", request);
      this.selectedRequest = request;
      this.showDeleteConfirmationModal = true;
    },
    confirmDeleteRequest() {
      console.log("Confirming deletion for request ID:", this.selectedRequest?.id);
      axios.post(`/api/s/${this.sponsorname}/dashboard`, { action: 'delete', request_id: this.selectedRequest.campaign_req_id, user_id: this.selectedRequest.user_id})
        .then(response => {
          console.log("Delete request response:", response.data);
          this.activeRequests = response.data.activeRequests;
          this.newRequests = response.data.newRequests;
          this.hideModal('DeleteConfirmationModal');
          setTimeout(() => {
            window.location.reload(true);
          }, 200); // 200 milliseconds to ensure modal hides first
        })
        .catch(error => {
          console.error("There was an error deleting the request!", error);
        });
    },
    showCancelConfirmation(request) {
      console.log("Showing cancel confirmation for request:", request);
      this.selectedRequest = request;
      this.showCancelConfirmationModal = true;
    },
    confirmCancelCampaign() {
      console.log("Confirming cancellation for request ID:", this.selectedRequest?.id);
      axios.post(`/api/s/${this.sponsorname}/dashboard`, { action: 'cancel', request_id: this.selectedRequest.campaign_req_id, user_id: this.selectedRequest.user_id })
        .then(response => {
          console.log("Cancel campaign response:", response.data);
          this.activeRequests = response.data.activeRequests;
          this.newRequests = response.data.newRequests;
          this.hideModal('CancelConfirmationModal');
        })
        .catch(error => {
          console.error("There was an error cancelling the campaign!", error);
        });
    },
    showCompleteConfirmation(request) {
      console.log("Showing complete confirmation for request:", request);
      axios.post(`/api/s/${this.sponsorname}/dashboard`, { action: 'complete', request_id: request.campaign_req_id, user_id: request.user_id })
        .then(response => {
          console.log("Complete campaign response:", response.data);
          this.activeRequests = response.data.activeRequests;
          this.newRequests = response.data.newRequests;
          this.hideModal('CompleteConfirmationModal');
        })
        .catch(error => {
          console.error("There was an error completing the campaign!", error);
        });
    },
    hideModal(modalName) {
      if (modalName === 'CampaignModal') {
        this.showCampaignModal = false;
      } else if (modalName === 'AcceptConfirmationModal') {
        this.showAcceptConfirmationModal = false;
      } else if (modalName === 'DeleteConfirmationModal') {
        this.showDeleteConfirmationModal = false;
      } else if (modalName === 'CancelConfirmationModal') {
        this.showCancelConfirmationModal = false;
      } else if (modalName === 'CompleteConfirmationModal') {
        this.showCompleteConfirmationModal = false;
      }  else if (modalName === 'RequestModal') {
        this.showRequestModal = false;
      } else if (modalName === 'RenegotiateModal') {
        this.showRenegotiateModal = false;
      }
    },

    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('role_id');
      localStorage.removeItem('username');
      this.$router.push('/sponsorlogin');
    }
  }
}
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

.modal.fade {
  display: none;
}
.modal.show {
  display: block;
  padding-right: 15px;
}
.modal {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  margin: auto;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}
</style>