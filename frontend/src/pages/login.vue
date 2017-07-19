<template>
  <div class="login">
    <h1 id='et'>{{ msg }}</h1>
    <div class="login-form-wrapper">
      <el-form :model="login" ref="login" label-width="70px">
        <el-form-item id=“username” label="用户名：">
          <el-input v-model="login.username"></el-input>
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="login.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="验证码：">
          <el-col :span="12">
            <el-input v-model="login.captcha"></el-input>
          </el-col>
          <el-col :span="8" :offset="1">
            <img v-bind:src="login.captcha_img" alt="验证码" @click="refresh_cap">
          </el-col>
          <el-col :span="6">
            <el-checkbox label="记住密码" v-model="login.remember"></el-checkbox>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="submit">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      msg: 'Welcome to Your Docker Manager',
      login: {
        username: '',
        password: '',
        captcha: '',
        remember: false,
        captcha_img: ''
      }
    }
  },
  methods: {
    submit () {
      var csrftoken = this.$cookie.get('csrftoken')
      var params = new URLSearchParams()
      var self = this

      params.append('username', self.login.username)
      params.append('password', self.login.password)
      params.append('captcha_0', self.$data.captcha_0_value)
      params.append('captcha_1', self.login.captcha)
      params.append('remember', self.login.remember)
      this.$ajax({
        method: 'post',
        url: '/login/',
        data: params,
        headers: {'X-CSRFTOKEN': csrftoken, 'Content-Type': 'application/x-www-form-urlencoded'}
      }).then(function (response) {
        if (response.data['msg'] === 'login success') {
          self.$router.push({ path: '/hello' })
        } else if (response.data['msg'] === 'Wrong username or password') {
          self.$message('用户名密码错误')
          self.login.captcha_img = response.data['img_src']
          self.$data.captcha_0_value = response.data['captcha_0']
        } else if (response.data['msg'] === 'Wrong captcha input') {
          self.$message('验证码错误')
          self.login.captcha_img = response.data['img_src']
          self.$data.captcha_0_value = response.data['captcha_0']
        }
      })
    },
    refresh_cap () {
      var self = this
      this.$ajax.get('/login/').then(function (response) {
        for (var item in response.data) {
          if (item === 'img_src') {
            self.login.captcha_img = response.data[item]
            self.$data.captcha_0_value = response.data['captcha_0']
          }
        }
      })
    }
  },
  mounted () {
    var self = this
    this.$ajax.get('/login/').then(function (response) {
      for (var item in response.data) {
        if (item === 'img_src') {
          self.login.captcha_img = response.data[item]
          self.$data.captcha_0_value = response.data['captcha_0']
        }
      }
    })
  },
  props: {
    captcha_0: ''
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

a {
  color: #42b983;
}


.login-form-wrapper {
  width: 360px;
  margin-left: 40%;
  margin-top: 120px;
  position: relative;
  .el-form {
    margin-top: 8%;
    margin-botton: 8%;
  }
}
</style>
