<template>
  <div id="app">
    <el-row>
      <login />
    </el-row>
    <el-row>
      <search />
    </el-row>
  </div>
</template>

<script>
import search from "./components/Search.vue";
import login from "./components/Login.vue";
export default {
  methods: {
    startHacking() {
      this.$notify({
        title: "It works!",
        type: "success",
        message:
          "We've laid the ground work for you. It's time for you to build something epic!",
        duration: 5000
      });
    }
  },
  components: {
    search,
    login
  },
  data() {
    return {
      searchData: ""
    };
  }
};
</script>

<style>
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
</style>
