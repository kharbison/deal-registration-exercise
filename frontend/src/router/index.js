import Vue from 'vue'
import VueRouter from 'vue-router'
import DealRegSearch from '../views/DealRegSearch.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'dealRegSearch',
    component: DealRegSearch
  }
]

const router = new VueRouter({
  routes
})

export default router
