// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import App from './App'
import router from './router'
import axios from 'axios'
import VueCookie from 'vue-cookie'

Vue.prototype.$ajax = axios
axios.defaults.baseURL = '/api'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueCookie)

export const get_user = function () {
  return sessionStorage.user
}

router.beforeEach((to, from, next) => {
  var is_auth = get_user()
  if (to.path === '/login/' && is_auth) {
    next({path: '/frontend/'})
  }
  if (!is_auth && to.path !== '/login/') {
    next({path: '/login/'})
  } else {
    next()
  }
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  render: h => h(App)
})

