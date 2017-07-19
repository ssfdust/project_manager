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

function getCookie (name) {
  var cookieValue = null
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i]
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

function get_auth_status () {
  var ret = false
  var t = getCookie('sessionid')
  console.log(t)
  if (getCookie('sessionid') !== null) {
    ret = true
  }
  return ret
}
router.beforeEach((to, from, next) => {
  var is_auth = get_auth_status()
  console.log('router function')
  if (to.path === '/login' && is_auth) {
    next({path: '/containers'})
  }
  if (!is_auth && to.path !== '/login') {
    next({path: '/login'})
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

