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
        <el-input class="username" size="small" v-model="username" placeholder="用户名"></el-input>
        <el-input class="password" size="small" v-model="password" placeholder="密码" show-password></el-input>
        <el-button class="login" size="small" type="primary">登录</el-button>
      </div>
      <el-button type="text" slot="reference">登录</el-button>
    </el-popover>
    <el-dropdown trigger="hover" v-show="user!=''">
      <span class="el-dropdown-link userinfo-inner">{{user}}</span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>设置</el-dropdown-item>
        <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import { searchEnginesData, searchEnginesAutoComplete } from "../api/search";

export default {
  name: "login",
  data() {
    return {
      username: "",
      password: "",
      user: "asdf"
    };
  },
  methods: {},
  created() {},
  mounted() {}
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
  font-size: 20px;
  cursor: pointer;
  color: rgb(23, 74, 168);
}
</style>
