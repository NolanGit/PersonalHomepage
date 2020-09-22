// 登录页不往父组件传递任何信息，登录/登出只会操作cookie后刷新页面以重加载父组件，父组件自行判断cookie状态
// 登录页接受三个参数，父组件从cookie获取的用户id、用户名、登录名
// 用户id用于判定按钮展示"登录"还是用户名，用户名用于在页面上展示，登录名用于传入子组件，便于修改用户信息（如改密码）时减少填写量
<template>
  <div class="login-button">
    <el-popover
      class="login-popover"
      placement="top"
      width="160"
      v-model="visible"
      v-show="user_id==0"
    >
      <div style="text-align: right; margin: 0">
        <el-input
          class="login_name"
          size="small"
          v-model="login_name"
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

    <el-dropdown class="user-popover" trigger="hover" v-show="user_id!=0">
      <span class="el-dropdown-link userinfo-inner">{{user_name}}</span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native="consoleClicked">控制台</el-dropdown-item>
        <el-dropdown-item @click.native="cloudClicked">网盘 / 图床</el-dropdown-item>
        <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>

    <el-drawer
      :title="drawer.title"
      :visible.sync="drawer.visible"
      :direction="drawer.direction"
      :size="drawer.size"
      :before-close="drawerBeforeClose"
    >
      <Console :user_id="user_id" :login_name="login_name" v-if="drawer.title=='控制台'" />
      <CloudDriveAndImageHosting
        :user_id="user_id"
        v-if="drawer.title=='网盘 / 图床'"
        @cloudStatusChanged="cloudStatusChanged"
      />
    </el-drawer>
  </div>
</template>
<script>
import md5 from "js-md5";
import axios from "axios";
import Router from "vue-router";
import Console from "./loginDropdowns/Console.vue";
import CloudDriveAndImageHosting from "./loginDropdowns/CloudDrive&ImageHosting.vue";
const api = {
  userLogin: "/login/userLogin",
  userLoginSalt: "/login/userLoginSalt"
};
export default {
  name: "login",
  components: {
    Console,
    CloudDriveAndImageHosting
  },
  props: {
    login_name: String,
    user_name: String,
    user_id: Number
  },
  data() {
    return {
      visible: false,
      password: "",
      salt: "",
      user: "",
      cloudStatus: 0,
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
    async login() {
      if (
        this.login_name === "" ||
        this.password === "" ||
        this.login_name === undefined ||
        this.password === undefined ||
        this.login_name.length == 0 ||
        this.password.length == 0
      ) {
        this.$notify.error({
          message: "请填写用户名和密码",
          type: "error"
        });
      } else {
        try {
          const { data: res } = await axios.post(api.userLoginSalt, {
            login_name: this.login_name
          });
          var para = {
            login_name: this.login_name,
            password: this.md5It(
              this.md5It(this.md5It(this.password) + res.data.stable_salt) +
                res.data.salt
            ),
            is_generate_cookie: true
          };
          const { data: res2 } = await axios.post(api.userLogin, para);
          this.visible = false;
          this.$message({
            message: res2.msg,
            type: "success"
          });
          this.$cookies.set("user_key", res2.user_key);
          this.$cookies.set(
            "user_name",
            JSON.stringify(res2.user_name).replace(/\"/g, "")
          );
          this.$cookies.set(
            "login_name",
            JSON.stringify(res2.login_name).replace(/\"/g, "")
          );
          this.$cookies.set("user_id", JSON.stringify(res2.user_id));
          location.reload();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      }
    },
    logout() {
      this.$cookies.remove("user_key");
      this.$cookies.remove("user_name");
      this.$cookies.remove("login_name");
      this.$cookies.remove("user_id");
      this.$message({
        message: "退出成功！",
        type: "success"
      });
      location.reload();
    },
    consoleClicked() {
      this.drawer.title = "控制台";
      this.drawer.size = "500";
      this.drawer.visible = true;
      this.drawer.direction = "ttb";
    },
    cloudClicked() {
      this.drawer.title = "网盘 / 图床";
      this.drawer.size = "50%";
      this.drawer.visible = true;
      this.drawer.direction = "rtl";
      this.cloudStatus = 0;
    },
    cloudStatusChanged(cloudStatus) {
      this.cloudStatus = cloudStatus;
    },
    //关闭窗口
    drawerBeforeClose(done) {
      if (this.cloudStatus == 1) {
        this.$confirm(
          "检测到您的文件仍在上传中，关闭页面会打断上传，仍然要关闭吗?",
          "提示",
          {}
        ).then(_ => {
          this.drawer.title = "";
          done();
          this.cloudStatus = 0;
        });
      } else {
        this.drawer.title = "";
        done();
      }
    }
  },
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
.login_name {
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
