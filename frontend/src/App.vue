<template>
  <div id="app">
    <el-row class="loginRow">
      <login v-if="loginSwitch" @user="userLoginedOrLogout" />
    </el-row>
    <el-row class="searchRow">
      <search />
    </el-row>
    <el-row class="cardRow">
      <el-col :span="8">
        <transition name="el-zoom-in-top">
          <el-card
            shadow="hover"
            v-show="show.weather"
            class="margin_left-medium margin_right-medium"
          >
            <weather @weatherLoaded="weatherLoaded" :locations="locations" :user="user" />
          </el-card>
        </transition>
      </el-col>
      <el-col :span="8">
        <el-card
          shadow="hover"
          v-show="show.bookmarks"
          class="margin_left-medium margin_right-medium"
        >
          <bookmarks :bookmarksData="bookmarksData" @bookmarksUpdate="userInfo" :user="user" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="margin_left-medium margin_right-medium">
          <appMonitor />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
import search from "./components/Search.vue";
import login from "./components/Login.vue";
import weather from "./components/Weather.vue";
import bookmarks from "./components/Bookmarks.vue";
import appMonitor from "./components/AppMonitor.vue";
export default {
  components: {
    search,
    login,
    weather,
    bookmarks,
    appMonitor
  },
  data() {
    return {
      user: "",
      locations: [],
      bookmarksData: [],
      show: {
        weather: false,
        bookmarks: false
      },
      loginSwitch: true
    };
  },
  methods: {
    async userInfo() {
      try {
        var user = sessionStorage.getItem("user").replace(/\"/g, "");
      } catch (error) {
        var user = undefined;
      }
      this.user = user;
      try {
        const { data: res } = await axios.post("/userInfo", {
          user: user
        });
        this.locations = res.data["locations"];
        this.bookmarksData = res.data["bookmarks"];
        this.show.bookmarks = true;
      } catch (e) {
        if (e.response.status == 401) {
          sessionStorage.removeItem("user");
          this.$cookies.remove("user_key");
          this.loginSwitch = false;
          this.$nextTick(() => {
            this.loginSwitch = true;
          });
        } else if (e.response.status == 403) {
          console.log(e.response.data.msg);
        } else {
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      }
    },
    userLoginedOrLogout(user) {
      if (user != "") {
        this.userInfo();
      } else {
        location.reload();
      }
    },
    weatherLoaded() {
      this.show.weather = true;
    }
  },
  mounted() {
    this.userInfo();
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
