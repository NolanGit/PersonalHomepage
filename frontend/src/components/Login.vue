<template>
  <div class="login-button">
    <el-popover
      class="login-popover"
      placement="top"
      width="160"
      v-model="visible"
      v-show="user==''"
    >
      <div style="text-align: right; margin: 0">
        <el-input
          class="username"
          size="small"
          v-model="username"
          placeholder="用户名"
          @keyup.enter.native="login()"
        ></el-input>
        <el-input
          class="password"
          size="small"
          v-model="password"
          placeholder="密码"
          show-password
          @keyup.enter.native="login()"
        ></el-input>
        <el-button class="login" size="small" type="primary" @click="login()">登录</el-button>
      </div>
      <el-button type="text" slot="reference">登录</el-button>
    </el-popover>
    <el-dropdown class="user-popover" trigger="hover" v-show="user!=''">
      <span class="el-dropdown-link userinfo-inner">{{user}}</span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native="consoleSettingClicked">控制台</el-dropdown-item>
        <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <el-drawer
      :title="drawer.title"
      :visible.sync="drawer.visible"
      :direction="drawer.direction"
      :size="drawer.size"
    >
      <Console />
    </el-drawer>
  </div>
</template>
<script>
import md5 from "js-md5";
import axios from "axios";
import Router from "vue-router";
import Console from "./Console.vue";
import { userLogin, userLoginGetSalt } from "../api/login";

export default {
  name: "login",
  components: {
    Console
  },
  data() {
    return {
      visible: false,
      username: "",
      password: "",
      salt: "",
      user: "",
      drawer: {
        title: "",
        size: "",
        visible: false,
        direction: "ttb"
      }
    };
  },
  methods: {
    md5It(str) {
      str = md5(str);
      return str;
    },
    login() {
      if (
        this.username === "" ||
        this.password === "" ||
        this.username === undefined ||
        this.password === undefined ||
        this.username.length == 0 ||
        this.password.length == 0
      ) {
        this.$notify.error({
          message: "请填写用户名和密码",
          type: "error"
        });
      } else {
        var para = {
          login_name: this.username
        };
        userLoginGetSalt(para).then(data => {
          if (data["code"] !== 200) {
            this.$message({
              message: data["msg"],
              type: "error"
            });
          } else {
            var para = {
              login_name: this.username,
              password: this.md5It(
                this.md5It(this.md5It(this.password) + data.data.stable_salt) +
                  data.data.salt
              ),
              timestamp: Math.round(new Date() / 1000)
            };
            userLogin(para).then(data2 => {
              if (data2["code"] !== 200) {
                this.$message({
                  message: data2.msg,
                  type: "error"
                });
              } else {
                this.visible = false;
                this.$message({
                  message: data2.msg,
                  type: "success"
                });
                this.$cookies.set("user_key", data2.user_key);
                this.user = data2.user;
                sessionStorage.setItem("user", JSON.stringify(data2.user));
                this.$emit("user", this.user);
              }
            });
          }
        });
      }
    },
    logout() {
      sessionStorage.removeItem("user");
      this.user = "";
      this.$message({
        message: "退出成功！",
        type: "success"
      });
      this.$cookies.remove("user_key");
      this.$emit("user", "");
    },
    consoleSettingClicked() {
      this.drawer.title = "控制台";
      this.drawer.size = "500";
      this.drawer.visible = true;
      this.drawer.direction = "ttb";
    }
  },
  created() {},
  mounted() {
    try {
      var user = sessionStorage.getItem("user").replace(/\"/g, "");
      this.user = user;
    } catch (error) {}
  }
};
</script>
<style scoped>
.login-button {
  position: absolute;
  right: 0px;
  top: 0px;
  z-index: 99;
  margin-right: 20px;
}
.username {
  padding-bottom: 3px;
}
.password {
  padding-bottom: 3px;
}
.login {
  text-align: center;
  margin-top: 3px;
}
.userinfo-inner {
  font-size: 14px;
  cursor: pointer;
  color: #409eff;
}
.user-popover {
  padding-top: 12px;
}
</style>
