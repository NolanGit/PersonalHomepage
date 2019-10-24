<template>
  <div id="app">
    <el-row class="loginRow">
      <login />
    </el-row>
    <el-row class="searchRow">
      <search />
    </el-row>
    <el-row class="cardRow">
      <el-col :span="7" :offset="1">
        <el-card shadow="hover">
          <weather :city="city" />
        </el-card>
      </el-col>
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
    return {
      city: "beijing"
    };
  }
};
</script>

<style>
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
.cardRow {
  padding-top: 40px;
}
</style>
