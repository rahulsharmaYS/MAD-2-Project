const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

// vue.config.js
module.exports = {
  devServer: {
    proxy: 'http://localhost:8000',
  },
};
