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
          <el-carousel :autoplay="false" height="250px">
            <el-carousel-item v-for="city in cities" :key="city">
              <weather :city="city" />
            </el-carousel-item>
            <el-carousel-item v-show="user!=''">
              <el-button icon="el-icon-circle-plus-outline" circle></el-button>
            </el-carousel-item>
          </el-carousel>
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
    try {
      var user = sessionStorage.getItem("user").replace(/\"/g, "");
      this.user = user;
    } catch (error) {}
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
