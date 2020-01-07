<template>
  <div class="console-main">
    <el-row class="margin_bottom-large">
      <el-col v-for="consoleOption in consoleOptions" :key="consoleOption" :span="5" :offset="1">
        <el-card class="box-card">
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
      <div class="margin-medium">
        <div v-if="activeComponent=='ConsoleScript'">
          <ConsoleScript />
        </div>
      </div>
    </el-drawer>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import ConsoleScript from "./console/ConsoleScript.vue";
import { consoleGet } from "../api/console";

export default {
  name: "Console",
  components: {
    ConsoleScript
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
      this.$emit("consoleOptionSelected");
      this.activeComponent = consoleOption.component_name;
      this.drawer.title = consoleOption.name;
      this.drawer.visible = true;
      this.drawer.direction = "ttb";
      this.drawer.size = "80%";
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
.margin-top-medium {
  margin-top: 20px;
}
.margin_bottom-medium {
  margin-bottom: 20px;
}
.margin_bottom-large {
  margin-bottom: 40px;
}
.margin_left-medium {
  margin-left: 20px;
}
.margin_right-small {
  margin-right: 10px;
}
.margin_right-medium {
  margin-right: 20px;
}
.margin-medium{
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-right: 20px;
}
</style>
