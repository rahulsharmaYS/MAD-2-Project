<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap");
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}

body {
    background: whitesmoke;
    /* background-size: cover; */
    display: block;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    width: device-width, initial-scale= 1, maximum-scale= 1,user-scalable= no;
    margin: 0;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #fff;
    margin: 0;
    padding: 0;
}


.dark {
    background: #1e1e1e;
}

.light {
    /* background: linear-gradient(45deg, #f095335d 0%, #2332d388 25%, #c3213974 50%, #cc2367b0 75%, #c84ca138 100%); */
    min-width: 100vw;
    background: whitesmoke;
}


.theme-toggle {
    position: fixed; 
    top: 10px;  
    right: 10px;
    padding: 8px 12px;
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    z-index: 1000;
    font-size: 10px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease-in-out;
}

.theme-toggle:hover {
    background-color: rgba(255, 255, 255, 1);
}


.full-height {
    height: 100vh; 
    width: 100vw; 
    /* max-width: 1200px;  */
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin: 0 auto; 
}
.welcome-section {
    flex: 1;
    text-align: center;
    padding: 20px;
    padding-left: 0;
    padding-right: 0;
    position: relative;
    left: 20px;
    color: #fff;
}

.welcome-section h1 {
    font-size: 3rem;
    font-family: cursive;
    font-weight: 600;
    line-height: 1.2;
    margin: 0;
    
}

.divider {
    width: 2px;
    height: 70%;
    background-color: rgba(255, 255, 255, 0.5);
    margin: 0 20px;
    position: relative;
    left: -140px;
}

.login-section {
    flex: 1;
    max-width: 400px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    position: relative;
    right: 120px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    text-align: center;
}

.login-section h2 {
    color: #fff;
    margin-bottom: 20px;
    font-size: 2rem;
}

.login-section .form-control {
    background: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 20px;
    width: 100%;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

.login-section .btn {
    width: 100%;
    border-radius: 20px;
    padding: 15px;
    background: none;
    border: 1px solid rgba(255, 255, 255, 0.5);
    color: #fff;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    cursor: pointer;
    font-size: medium;
}

.login-section .text-link {
    color: #fff;
    text-decoration: underline;
    cursor: pointer;
}

.login-section .btn-info, .login-section .btn-warning {
    margin-top: 10px;
}

@media (max-width: 768px) {
    .welcome-section h1 {
        font-size: 2rem;
    }

    .login-section {
        padding: 20px;
    }

    .login-section h2 {
        font-size: 1.5rem;
    }

    .login-section .form-control {
        padding: 12px;
    }

    .login-section .btn {
        padding: 12px;
    }
}

@media (max-width: 576px) {
    .full-height {
        flex-direction: column;
        justify-content: flex-start;
        padding: 20px;
    }

    .welcome-section {
        margin-bottom: 20px;
    }

    .divider {
        display: none;
    }

    .login-section {
        padding: 15px;
        width: 100%;
    }

    .login-section h2 {
        font-size: 1.2rem;
    }

    .login-section .form-control {
        padding: 10px;
    }

    .login-section .btn {
        padding: 10px;
    }
}

.component-wrapper {
    position: relative;
}

.back-button {
    position: absolute;
    top: -29px;
    right: -25px;
    font-size: 1.5em;
    color: #ffffff95;
    text-decoration: none;
}

.back-button:hover {
    color: #ffffff;
}

.back-button i {
    cursor: pointer;
}

.select-wrapper {
    position: relative;
    display: inline-block;
    width: 100%;
}

.select-wrapper select {
    width: 100%;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background: none;
    border: 1px solid #ccc;
    padding: 0.5rem;
    padding-right: 2.5rem;
    border-radius: 4px;
}

.select-wrapper::after {
    content: '\f078';
    font-family: 'Font Awesome 5 Free';
    font-weight: 900;
    position: absolute;
    top: 40%;
    right: 15px;
    transform: translateY(-50%);
    pointer-events: none;
}

.form-control-sm {
    font-size: 0.875rem;
}

.social-media-icon {
    width: 1.5rem;
    height: 1.5rem;
    margin-right: 0.5rem;
}
</style>

<template>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <div :class="{ 'dark': darkTheme, 'light': !darkTheme }" class="full-height" style="position: relative;">
      <router-view></router-view>
      <button @click="toggleTheme" class="theme-toggle">Theme</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'App',
    data() {
      return {
        darkTheme: true
      };
    },
    methods: {
      toggleTheme() {
        this.darkTheme = !this.darkTheme;
        localStorage.setItem('darkTheme', this.darkTheme ? 'dark' : 'light');
        document.body.classList.toggle('dark', this.darkTheme);
        document.body.classList.toggle('light', !this.darkTheme);
      }
    },
    created() {
      const theme = localStorage.getItem('darkTheme');
      this.darkTheme = (theme === 'dark');
      document.body.classList.toggle('dark', this.darkTheme);
      document.body.classList.toggle('light', !this.darkTheme);
    }
  };
  </script>
  
  <style>
  @import 'bootstrap/dist/css/bootstrap.min.css';
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap");
  @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
  }
  
  body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
  }
  
  .dark {
    background: #1e1e1e;
  }
  
  .light {
    background: linear-gradient(45deg, #f0953379 0%, #2331d3c0 25%, #c32139d6 50%, #cc2367b0 75%, #c84ca1a9 100%);
    min-width: 100vw;
    backdrop-filter: blur(20px);
    background-color: rgba(255, 255, 255, 0.222);  
  }
  
  .full-height {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .navbar {
    position: fixed; 
    width: 100%;
    z-index: 999;
    left: 0;
    top: 0;
    padding-left: 0;
    padding-right: 0;
  }
  
  .navbar-nav {
    display: flex;
    justify-content: flex-end;
  }
  
  .navbar-nav .nav-item {
    margin-left: 10px;
  }
  
  .theme-toggle {
    position: fixed;
    top: 15px;
    right: 15px;
    padding: 8px 12px;
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    z-index: 1000;
    font-size: 10px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease-in-out;
  }
  
  .theme-toggle:hover {
    background-color: rgba(255, 255, 255, 1);
  }
  
  .container {
    margin-top: 80px;
    padding: 20px;
  }
  
  .modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
  }
  
  .modal.fade.show.d-block {
    display: block;
  }
  
  .modal-dialog {
    margin: 15px auto;
  }
  
  .modal-content {
    background: white;
    border-radius: 5px;
  }
  
  @media (max-width: 768px) {
    .theme-toggle {
      font-size: 12px;
      top: 20px;
      right: 20px;
    }
  
    .container {
      padding: 10px;
    }
  }
  
  @media (max-width: 576px) {
    .navbar {
      padding: 0;
    }
  }
  </style>