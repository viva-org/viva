// src/stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isLoggedIn: false,
  }),

  actions: {
    setUser(user) {
      this.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },

    setLoggedIn(status) {
      this.isLoggedIn = status
      localStorage.setItem('isLoggedIn', status)
    },

    initializeStore() {
      const savedUser = localStorage.getItem('user')
      const savedLoginStatus = localStorage.getItem('isLoggedIn')
      
      if (savedUser) {
        this.user = JSON.parse(savedUser)
      }
      
      if (savedLoginStatus) {
        this.isLoggedIn = savedLoginStatus === 'true'
      }
    },

    logout() {
      this.user = null
      this.isLoggedIn = false
      localStorage.removeItem('user')
      localStorage.removeItem('isLoggedIn')
    },
  },
  
  getters: {
    getUser: (state) => state.user,
    getLoginStatus: (state) => state.isLoggedIn,
  },
})