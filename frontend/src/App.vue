<template>
  <div id="app">
    <el-row>
      <login />
    </el-row>
    <el-row>
      <search />
    </el-row>
    <el-row>
      <weather />
    </el-row>
  </div>
</template>

<script>
import search from "./components/Search.vue";
import login from "./components/Login.vue";
import weather from "./components/Weather.vue";
export default {
  methods: {},
  components: {
    search,
    login,
    weather
  },
  data() {
    return {};
  }
};
</script>

<style>
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
</style>
