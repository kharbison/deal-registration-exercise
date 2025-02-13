import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'dealRegSearch',
    component: () => import('@/views/DealRegSearch.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
