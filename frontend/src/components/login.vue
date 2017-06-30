<template>
  <div class="login">
    <h1>{{ msg }}</h1>
    <el-button @click="visible = true">按钮</el-button>
    <el-dialog v-model="visbile" title="Hello world">
      <p>欢迎使用element</p>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      msg: 'Welcome to Your Element-UI App',
      visbile: false
    }
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
</style>
