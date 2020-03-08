<template>
  <div class="console-main">
    <el-row class="margin_bottom-large">
      <el-col v-for="consoleOption in consoleOptions" :key="consoleOption" :span="5" :offset="1">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>{{consoleOption.name}}</span>
          </div>
          <i :class="consoleOption.icon" style="font-size: 30px;"></i>
          <el-button
            style="float: right"
            size="small"
            @click="consoleOptionClicked(consoleOption)"
          >进入</el-button>
        </el-card>
      </el-col>
    </el-row>
    <el-drawer
      :title="drawer.title"
      :visible.sync="drawer.visible"
      :direction="drawer.direction"
      :size="drawer.size"
    >
      <div class="margin-medium" v-if="drawer.visible==true">
        <div v-if="activeComponent=='ConsoleScript'">
          <ConsoleScript />
        </div>
        <div v-if="activeComponent=='ConsolePrivilege'">
          <ConsolePrivilege />
        </div>
      </div>
    </el-drawer>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import ConsoleScript from "./console/ConsoleScript.vue";
import ConsolePrivilege from "./console/ConsolePrivilege.vue";
import { consoleGet } from "../api/console";

export default {
  name: "Console",
  components: {
    ConsoleScript,
    ConsolePrivilege
  },
  data() {
    return {
      consoleOptions: [],
      drawer: {
        title: "",
        size: "",
        visible: false,
        direction: "ttb"
      },
      activeComponent: ""
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
        }
      });
    },
    consoleOptionClicked(consoleOption) {
      this.activeComponent = consoleOption.component_name;
      this.drawer.title = consoleOption.name;
      this.drawer.visible = true;
      this.drawer.direction = "ttb";
      this.drawer.size = "80%";
    }
  },
  created() {},
  mounted() {
    this.consoleGetFront();
  }
};
</script>
<style scoped>
</style>
