<template>
  <div id="app">
    <el-row class="loginRow">
      <login @user="userLoginedOrLogout" />
    </el-row>
    <el-row class="searchRow">
      <search />
    </el-row>
    <el-row class="cardRow">
      <el-col :span="7" :offset="1">
        <transition name="el-zoom-in-top">
          <el-card shadow="hover" v-show="show.weather">
            <weather @weatherLoaded="weatherLoaded" :locations="locations" :user="user" />
          </el-card>
        </transition>
      </el-col>
      <el-col :span="7" :offset="1">
        <el-card shadow="hover" v-show="show.weather">
          <bookmarks :bookmarksData="bookmarksData" :user="user" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import search from "./components/Search.vue";
import login from "./components/Login.vue";
import weather from "./components/Weather.vue";
import bookmarks from "./components/Bookmarks.vue";
import { userInfo } from "./api/app";
export default {
  components: {
    search,
    login,
    weather,
    bookmarks
  },
  data() {
    return {
      user: "",
      locations: [],
      bookmarksData: [],
      show: {
        weather: false
      }
    };
  },
  methods: {
    userInfoFront() {
      try {
        var user = sessionStorage.getItem("user").replace(/\"/g, "");
      } catch (error) {
        var user = undefined;
      }
      this.user = user;
      var para = {
        user: user
      };
      userInfo(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.locations = data.data["locations"];
          this.bookmarksData = data.data["bookmarks"];
        }
      });
    },
    userLoginedOrLogout(user) {
      if (user != "") {
        this.userInfoFront();
      } else {
        location.reload();
      }
    },
    weatherLoaded() {
      this.show.weather = true;
    }
  },
  created() {
    this.userInfoFront();
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
