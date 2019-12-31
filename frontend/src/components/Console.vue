<template>
  <div class="console-main">
    <div class="div-flex">
      <el-row>
        <el-col v-for="consoleOption in consoleOptions" :key="consoleOption" :span="5" :offset="1">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>{{consoleOption.name}}</span>
            </div>
            <i :class="consoleOption.icon"></i>
            <el-button style="float: right; padding: 3px 0" type="text">进入</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>
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
    this.consoleGetFront();
  }
};
</script>
<style scoped>
.div-flex {
  display: flex;
}
.text-mini {
  font-size: 10px;
}
.text-small {
  font-size: 14px;
}
.text-medium {
  font-size: 20px;
}
.margin_right-small {
  margin-right: 10px;
}
.margin_left-medium {
  margin-left: 20px;
}
.margin_bottom-medium {
  margin-bottom: 20px;
}
.margin_bottom-large {
  margin-bottom: 40px;
}
.margin-top-medium {
  margin-top: 20px;
}
</style>
