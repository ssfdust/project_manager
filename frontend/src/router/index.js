import Vue from 'vue'
import Router from 'vue-router'
import login from '../pages/login'
import frontend from '../pages/frontend'
import backend from '../pages/backend'
import changepass from '../pages/changepass'
import logout from '../pages/logout'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      hide: true,
      component: login
    },
    {
      path: '/changepass',
      name: 'changepass',
      component: changepass
    },
    {
      path: '/logout',
      name: 'logout',
      component: logout
    },
    {
      path: '/frontend',
      header: true,
      name: '前端管理',
      component: frontend
    },
    {
      path: '/backend',
      header: true,
      name: '后端管理',
      component: backend
    }
  ]
})
