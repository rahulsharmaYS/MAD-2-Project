<template>
  <body style="background: blue;">
  <div class="banned-page">
    <nav class="navbar navbar-expand-lg navbar-light bg-dark shadow-sm">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">SponsorNet</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/sponsorlogin" class="nav-link">Login</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="confirmation-wrapper">
      <div class="confirmation-details text-center">
        <h1 class="error-symbol">:(</h1>
        <h5 class="error-message">Sorry, {{ sponsorname }}!</h5>
        <p>You have been banned from our platform!</p>
        <p>Please try logging in later!</p>
      </div>
    </div>
  </div></body>
</template>

<script>
export default {
  data() {
    return {
      sponsorname: ''
    };
  },
  created() {
    this.sponsorname = this.$route.params.sponsorname;
  }
};
</script>

<style scoped>
.banned-page {
  background-color: whitesmoke;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.navbar {
  background-color: #007bff;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}

.navbar-brand, .nav-link {
  color: #fff !important;
}

.confirmation-wrapper {
  background-color: lightslategray;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.error-symbol {
  font-size: 4em;
  font-weight: bold;
  margin: 0;
}

.error-message {
  font-size: 1.5em;
  font-weight: bold;
}
</style>