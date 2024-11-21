<template>
    <body style="background:transparent; width: 100vw; height: 100vh;">
            <nav class="navbar navbar-expand-lg navbar-light bg-dark shadow-sm" style="background-color: #007bff; position:fixed; top:0; left:0; width:100%; z-index:999;">
            <div class="container-fluid">
              <router-link to="/sponsorlogin" class="navbar-brand" style="color: #fff;">SponsorNet</router-link>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                  <li class="nav-item">
                    <router-link to="/sponsorlogin" class="nav-link" style="color: #fff; position: relative; right: 100px;">Login ↩ </router-link>
                  </li>
                </ul></div></div></nav>
        <div class="confirmation-wrapper" style="background: transparent; width: 100vw; height: 100vh;">
          <div class="confirmation-details text-center">
            <h3 class="mt-4" style="color: darkslategrey;">Thank you, {{ sponsorname }}!</h3>
            <p style="color: darkslategrey;">Your application has been submitted. Please wait for admin approval.</p>
          </div></div>
      </body>
</template>

<script>
    export default{
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
