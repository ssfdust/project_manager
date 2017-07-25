<template>
  <div class="changepass">
    <head-top></head-top>
    <h1>{{ title }}</h1>
  </div>
</template>

<script>
  import header from '../components/head'
  export default {
    data () {
      return {
        title: 'Change Password'
      }
    },
    components: {
      'head-top': header
    }
  }
</script>
