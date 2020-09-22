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
        <div v-if="activeComponent=='Privilege'">
          <Privilege :user_id="user_id" :login_name="login_name" />
        </div>
        <div v-if="activeComponent=='Script'">
          <Script :user_id="user_id" />
        </div>
        <div v-if="activeComponent=='widgetEdit'">
          <widgetEdit :user_id="user_id" />
        </div>
      </div>
    </el-drawer>
  </div>
</template>
<script>
import axios from "axios";
import Privilege from "./console/Privilege.vue";
import Script from "./console/Script.vue";
import widgetEdit from "./console/WidgetEdit.vue";
const api = {
  get: "/console/get",
};

export default {
  name: "Console",
  props: {
    user_id: Number,
    login_name: String,
  },
  components: {
    Script,
    Privilege,
    widgetEdit,
  },
  data() {
    return {
      consoleOptions: [],
      drawer: {
        title: "",
        size: "",
        visible: false,
        direction: "ttb",
      },
      activeComponent: "",
    };
  },
  methods: {
    async consoleGetFront() {
      try {
        const { data: res } = await axios.get(api.get);
        this.consoleOptions = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    consoleOptionClicked(consoleOption) {
      this.activeComponent = consoleOption.component_name;
      this.drawer.title = consoleOption.name;
      this.drawer.visible = true;
      this.drawer.direction = "ttb";
      this.drawer.size = "80%";
    },
  },
  created() {},
  mounted() {
    this.consoleGetFront();
  },
};
</script>
<style scoped>
</style>
