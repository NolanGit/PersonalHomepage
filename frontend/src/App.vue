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
        <el-card shadow="hover">
          <weather :locations="locations" :user="user" />
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
      locations: [""]
    };
  },
  methods: {
    userInfoFront() {
      var user = sessionStorage.getItem("user").replace(/\"/g, "");
      if (user != undefined) {
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
          }
        });
      }
    },
    userLogined(user) {
      if (user != "") {
        this.userInfoFront();
      } else {
        window.reload();
      }
    }
  },
  mounted() {
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
