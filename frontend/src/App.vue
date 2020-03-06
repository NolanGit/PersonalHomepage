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
            <weather :userID="userID" @done="done('weather')" :locations="locations" :user="user" />
          </el-card>
        </transition>
      </el-col>
      <el-col :span="8">
        <transition name="el-zoom-in-top">
          <el-card
            shadow="hover"
            v-show="show.bookmarks"
            class="margin_left-medium margin_right-medium"
          >
            <bookmarks :bookmarksData="bookmarksData" :userID="userID" @bookmarksUpdate="userInfo" @done="done('bookmarks')"  />
          </el-card>
        </transition>
      </el-col>
      <el-col :span="8">
        <transition name="el-zoom-in-top">
          <el-card shadow="hover" v-show="show.app" class="margin_left-medium margin_right-medium">
            <appMonitor :user="user" :userID="userID" @done="done('app')" />
          </el-card>
        </transition>
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
const api = {
  userInfo: "/userInfo",
  widget: "/widget"
};
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
      userID: 0,
      widget:[],
      locations: [],
      bookmarksData: [],
      show: {
        weather: false,
        bookmarks: false,
        app: false
      },
      loginSwitch: true
    };
  },
  methods: {
    async userInfo() {
      try {
        const { data: res } = await axios.post(api.userInfo, {
          user_id: this.userID
        });
      } catch (e) {
        if (e.response.status == 401) {
          this.$cookies.remove("user_key");
          this.$cookies.remove("user");
          this.$cookies.remove("userID");
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
    async widgetGet() {
      try {
        const { data: res } = await axios.post(api.widget, {
          user_id: this.userID
        });
        this.widget = res.data;
        console.log(this.widget)
      } catch (e) {
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    userLoginedOrLogout(user) {
      if (user != "") {
        this.widgetGet();
      } else {
        location.reload();
      }
    },
    weatherLoaded() {
      this.show.weather = true;
    },
    done(para) {
      switch (para) {
        case "weather":
          this.show.weather = true;
          break;
        case "bookmarks":
          this.show.bookmarks = true;
          break;
        case "app":
          this.show.app = true;
          break;
      }
    }
  },
  created() {
    try {
      this.user = this.$cookies.get("user").replace(/\"/g, "");
      this.userID = this.$cookies.get("userID").replace(/\"/g, "");
    } catch (error) {
      this.user = "";
      this.userID = 0;
    }
  },
  mounted() {
    this.userInfo();
    this.widgetGet();
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
