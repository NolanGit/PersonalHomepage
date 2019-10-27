<template>
  <div id="app">
    <el-row class="loginRow">
      <login @user="userLogined" />
    </el-row>
    <el-row class="searchRow">
      <search />
    </el-row>
    <el-row class="cardRow">
      <el-col :span="7" :offset="1">
        <el-card shadow="hover">
          <weather :cities="cities" :user="user" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import search from "./components/Search.vue";
import login from "./components/Login.vue";
import weather from "./components/Weather.vue";
import { userInfo } from "./api/app";
export default {
  components: {
    search,
    login,
    weather
  },
  data() {
    return {
      user: "",
      cities: [""]
    };
  },
  methods: {
    userLogined(user) {
      this.user = user;
    }
  },
  mounted() {
    var user = sessionStorage.getItem("user").replace(/\"/g, "");
    this.user = user == undefined ? "" : user;
    console.log(this.user);
  }
};
</script>

<style>
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
.cardRow {
  padding-top: 120px;
}
</style>
