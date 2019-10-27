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
          <el-carousel>
            <el-carousel-item v-for="city in cities" :key="city">
              <weather :city="city" />
              <el-button v-show="user!=''" type="primary">主要按钮</el-button>
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
