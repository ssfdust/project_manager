<template>
  <div class="header_container">
    <el-menu theme="dark" :default-active="$route.matched[0].path" mode="horizontal" router>
      <el-row>
        <el-col :span="22">
          <el-menu-item
            v-for="(route, index) in $router.options.routes"
            v-if="route.header"
            :index="route.path" :key="index"
          >
          {{ route.name }}
          </el-menu-item>
        </el-col>
        <el-col :span="2">
          <el-submenu index="3" id="submenu" style="left:0%;">
            <template slot="title">{{ username }}</template>
            <el-menu-item index="/changepass">修改密码</el-menu-item>
            <el-menu-item index="">退出</el-menu-item>
          </el-submenu>
        </el-col>
      </el-row>
    </el-menu>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        username: sessionStorage.user
      }
    }
  }
</script>
<style>
  .header_container {
    margin: 0px;
  }

  .hidden {
    width:78%;
  }
</style>

