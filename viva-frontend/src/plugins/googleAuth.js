import vue3GoogleLogin from 'vue3-google-login'

export default {
  install: (app) => {
    app.use(vue3GoogleLogin, {
      clientId: '145000233203-68qjqeimootonnuv999os54ni9s0k14g.apps.googleusercontent.com'
    })
  }
}