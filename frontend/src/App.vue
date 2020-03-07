<template>
  <div id="app">
    <el-row class="loginRow">
      <login v-if="loginSwitch" @user="userLoginedOrLogout" />
    </el-row>
    <el-row class="searchRow">
      <search />
    </el-row>
    <div class="cardRow div-flex">
      <el-col :span="singleWidget.span" v-for="singleWidget in widget" :key="singleWidget">
        <transition name="el-zoom-in-top">
          <el-card
            shadow="hover"
            v-show="singleWidget.show==true"
            class="margin_left-medium margin_right-medium"
          >
            <weather
              v-if="singleWidget.name=='weather'"
              :user_id="user_id"
              @done="done('weather')"
            />
            <bookmarks
              v-if="singleWidget.name=='bookmarks'"
              :user_id="user_id"
              @done="done('bookmarks')"
            />
            <appMonitor v-if="singleWidget.name=='app'" :user_id="user_id" @done="done('app')" />
          </el-card>
        </transition>
      </el-col>
    </div>
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
      user_id: 0,
      widget: [],
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
          user_id: this.user_id
        });
      } catch (e) {
        if (e.response.status == 401) {
          this.$cookies.remove("user_key");
          this.$cookies.remove("user");
          this.$cookies.remove("user_id");
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
          user_id: this.user_id
        });
        this.widget = res.data;
        for (let x = 0; x < this.widget.length; x++) {
          this.widget[x].show = false;
        }
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
      for (let x = 0; x < this.widget.length; x++) {
        if (this.widget[x].name == para) {
          this.$nextTick(() => {
            this.widget[x].show = true;
          });
          break;
        }
      }
    }
  },
  created() {
    try {
      this.user = this.$cookies.get("user").replace(/\"/g, "");
      this.user_id = this.$cookies.get("user_id").replace(/\"/g, "");
    } catch (error) {
      this.user = "";
      this.user_id = 0;
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
