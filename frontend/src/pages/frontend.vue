<template>
  <div class="frontend">
    <head-top></head-top>
    <el-row class="switcher">
      <el-col :span="3" style="float:left;">
        <b>当前状态：{{ contain_status }}</b>
      </el-col>
      <el-col :span="5" style="float:right;">
        <span class="wrapper">
          <el-button :type="status" @click="switcher">{{ condition_button }}</el-button>
          <el-button type="warning">重启</el-button>
          <el-button type="info">下载日志</el-button>
        </span>
      </el-col>
    </el-row>
    <h1>{{ title }}</h1>
  </div>
</template>

<script>
  import header from '../components/head'
  export default {
    data () {
      return {
        title: 'Frontend',
        contain_status: '关闭',
        condition_button: '开启',
        status: 'success'
      }
    },
    components: {
      'head-top': header
    },
    methods: {
      switcher () {
        console.log(this.contain_status)
      }
    }
  }
</script>

<style>
  .switcher {
    padding:14px;
  }
</style>
