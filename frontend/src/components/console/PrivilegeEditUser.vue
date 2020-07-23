<template>
  <section>
    <el-row class="main-row" :gutter="20">
      <div v-if="action=='edit'">
        <div class="div-flex margin_bottom-medium margin_left-large" v-if="!isCheckedPass">
          <div class="td__p--label td--label">请输入原密码：</div>
          <el-input
            class="width--medium margin_right-small"
            show-password
            v-model="password"
            size="small"
            placeholder="请输入"
          ></el-input>
          <el-button type="primary" size="mini" plain @click="checkPass()">验证</el-button>
        </div>
        <div v-if="isCheckedPass">
          <div class="div-flex margin_bottom-medium margin_left-large">
            <div class="td__p--label td--label">请输入新密码：</div>
            <el-input
              class="width--medium margin_right-small"
              show-password
              v-model="passwordNew"
              size="small"
              placeholder="请输入"
            ></el-input>
            <el-button type="primary" size="mini" plain @click="changePass()">提交</el-button>
          </div>
          <div class="div-flex margin_bottom-medium margin_left-large">
            <div class="td__p--label td--label">请选择角色：</div>
            <el-select
              class="width--medium margin_right-small"
              v-model="role_id"
              size="small"
              placeholder="请选择"
            >
              <el-option
                v-for="item in roleData"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
            <el-button type="primary" size="mini" plain @click="changeRole()">提交</el-button>
          </div>
        </div>
      </div>
      <div class="margin_left-large" v-if="action=='new'">
        <div class="div-flex margin_bottom-medium">
          <div class="td__p--label td--label">请输入用户名称：</div>
          <el-input
            class="width--medium margin_right-small"
            v-model="username"
            size="small"
            placeholder="请输入"
          ></el-input>
        </div>
        <div class="div-flex margin_bottom-medium">
          <div class="td__p--label td--label">请输入用户登录名：</div>
          <el-input
            class="width--medium margin_right-small"
            v-model="login_name"
            size="small"
            placeholder="请输入"
          ></el-input>
        </div>
        <div class="div-flex margin_bottom-medium">
          <div class="td__p--label td--label">请输入用户密码：</div>
          <el-input
            class="width--medium margin_right-small"
            v-model="passwordNew"
            show-password
            size="small"
            placeholder="请输入"
          ></el-input>
        </div>
        <div class="div-flex margin_bottom-medium">
          <div class="td__p--label td--label">请选择角色：</div>
          <el-select
            class="width--medium margin_right-small"
            v-model="role_id"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in roleData"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </div>
        <el-button type="primary" size="mini" plain @click="userAddFront()">提交</el-button>
      </div>
    </el-row>
  </section>
</template>

<script>
import md5 from "js-md5";
import axios from "axios";
const api = {
  userGet: "/privilege/userGet",
  roleGet: "/privilege/roleGet",
  userRoleChange: "/privilege/userRoleChange",
  userLogin: "/login/userLogin",
  userLoginSalt: "/login/userLoginSalt",
  userChangePassword: "/login/userChangePassword",
  userAdd: "/login/userAdd"
};
export default {
  name: "PrivilegeEditUser",
  props: {
    user_id: Number,
    login_name: String,
    action: String
  },
  data() {
    return {
      username: "",
      password: "",
      passwordNew: "",
      isCheckedPass: false,
      role_id: "",
      roleData: []
    };
  },
  methods: {
    md5It(str) {
      str = md5(str);
      return str;
    },
    randomString(len) {
      len = len || 32;
      var $chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      var maxPos = $chars.length;
      var pwd = "";
      for (let i = 0; i < len; i++) {
        pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
      }
      return pwd;
    },
    async userGetFront() {
      try {
        const { data: res } = await axios.post(api.userGet, {
          user_id: this.user_id
        });
        this.userData = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async roleGetFront() {
      try {
        const { data: res } = await axios.get(api.roleGet);
        for (let x = 0; x < res.data.length; x++) {
          if (res.data[x].is_valid == 1) {
            this.roleData.push({
              label: res.data[x].name,
              value: res.data[x].id
            });
          }
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async checkPass() {
      if (
        this.password === "" ||
        this.password === undefined ||
        this.password.length == 0
      ) {
        this.$message({
          message: "请填写密码",
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
            is_generate_cookie: false
          };
          const { data: res2 } = await axios.post(api.userLogin, para);
          this.$message({
            message: res2.msg,
            type: "success"
          });
          this.isCheckedPass = true;
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      }
    },
    async changePass() {
      var stable_salt = this.randomString(40);
      var para = {
        login_name: this.login_name,
        stable_salt: stable_salt,
        password: this.md5It(this.md5It(this.passwordNew) + stable_salt)
      };
      try {
        const { data: res } = await axios.post(api.userChangePassword, para);
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.passwordNew = "";
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async changeRole() {
      try {
        const { data: res } = await axios.post(api.userRoleChange, {
          role_id: this.role_id,
          login_name: this.login_name
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.passwordNew = "";
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    async userAddFront() {
      if (
        this.username === "" ||
        this.username === undefined ||
        this.username.length == 0 ||
        this.passwordNew === "" ||
        this.passwordNew === undefined ||
        this.passwordNew.length == 0 ||
        this.role_id == ""
      ) {
        this.$message({
          message: "请将表单填写完整后提交",
          type: "error"
        });
      } else {
        var stable_salt = this.randomString(40);
        var para = {
          name: this.username,
          role_id: this.role_id,
          login_name: this.login_name,
          stable_salt: stable_salt,
          password: this.md5It(this.md5It(this.passwordNew) + stable_salt)
        };
        try {
          const { data: res } = await axios.post(api.userAdd, para);
          this.$message({
            message: res["msg"],
            type: "success"
          });
          this.$emit("close");
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      }
    }
  },
  mounted() {
    this.isCheckedPass = false;
    this.roleGetFront();
  }
};
</script>

<style scoped>
</style>