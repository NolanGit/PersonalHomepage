<template>
  <div id="app">
    <el-row class="loginRow">
      <login :user_id="user_id" :user_name="user_name" :login_name="login_name" />
    </el-row>
    <el-row class="searchRow">
      <search :user_id="user_id" />
    </el-row>
    <div class="cardRow div-flex">
      <el-col :span="singleWidget.span" v-for="(singleWidget,index) in widget" :key="singleWidget">
        <transition name="el-zoom-in-top">
          <el-card
            shadow="hover"
            v-show="singleWidget.show"
            class="margin_left-medium margin_right-medium"
          >
            <weather v-if="singleWidget.name=='weather'" :user_id="user_id" @done="done(index)" />
            <bookmarks
              v-if="singleWidget.name=='bookmarks'"
              :user_id="user_id"
              @done="done(index)"
            />
            <appMonitor v-if="singleWidget.name=='app'" :user_id="user_id" @done="done(index)" />
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
      widget: []
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
          this.user = "";
          this.user_id = 0;
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
        for (let x = 0; x < res.data.length; x++) {
          res.data[x].show = false;
        }
        this.widget = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    userIdFlush() {
      try {
        this.user_name = this.$cookies.get("user_name").replace(/\"/g, "");
        this.user_id = this.$cookies.get("user_id");
        this.login_name = this.$cookies.get("login_name");
      } catch (error) {
        this.user_name = "";
        this.user_id = 0;
        this.login_name = "";
      }
    },
    done(index) {
      this.widget[index].show = true;
    }
  },
  created() {
    this.userIdFlush();
  },
  mounted() {
    this.userInfo();
    this.userIdFlush();
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
