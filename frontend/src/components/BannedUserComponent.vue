<template>
  <div class="banned-page" style="position: relative; width: 100vw;">
    <nav class="navbar navbar-expand-lg navbar-light bg-dark shadow-sm">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">SponsorNet</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item" style="position: relative; right: 80px;">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="confirmation-wrapper" style="width: 100vw; position: relative; left: 25px;">
      <div class="confirmation-details text-center">
        <h1 class="error-symbol">:(</h1>
        <h5 class="error-message">Sorry, {{ username }}!</h5>
        <p>You have been banned from our platform!</p>
        <p>Please try logging in later!</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: ''
    };
  },
  created() {
    this.username = this.$route.params.username;
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