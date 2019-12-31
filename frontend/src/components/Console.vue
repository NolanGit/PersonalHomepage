<template>
  <div class="console-main">
    <el-card class="box-card" v-for="consoleOption in consoleOptions" :key="consoleOption">
      <div slot="header" class="clearfix">
        <span>{{consoleOption.name}}</span>
      </div>
      <i :class="consoleOption.icon"></i>
      <el-button style="float: right; padding: 3px 0" type="text">进入</el-button>
    </el-card>
    <el-drawer
      :title="drawer.title"
      :visible.sync="drawer.visible"
      :direction="drawer.direction"
      :size="drawer.size"
    ></el-drawer>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import { consoleGet } from "../api/console";

export default {
  name: "Console",
  data() {
    return {
      consoleOptions: [],
      drawer: {
        title: "",
        size: "",
        visible: false,
        direction: "ttb"
      }
    };
  },
  methods: {
    consoleGetFront() {
      consoleGet().then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.consoleOptions = data.data;
          console.log(this.consoleOptions);
        }
      });
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
</style>
