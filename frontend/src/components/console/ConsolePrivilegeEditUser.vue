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
            v-model="userNameNew"
            size="small"
            placeholder="请输入"
          ></el-input>
        </div>
        <div class="div-flex margin_bottom-medium">
          <div class="td__p--label td--label">请输入用户登录名：</div>
          <el-input
            class="width--medium margin_right-small"
            v-model="loginNameNew"
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
import { userGet, roleGet, userRoleChange } from "../../api/privilege";
import {
  userLogin,
  userLoginGetSalt,
  userChangePassword,
  userAdd
} from "../../api/login";
export default {
  name: "ConsolePrivilegeEditUser",
  props: {
    login_name: String,
    action: String
  },
  data() {
    return {
      userNameNew: "",
      loginNameNew: "",
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
    userGetFront() {
      var para = {
        user: sessionStorage.getItem("user").replace(/\"/g, "")
      };
      userGet(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.userData = data.data;
        }
      });
    },
    roleGetFront() {
      roleGet().then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          for (let x = 0; x < data.data.length; x++) {
            if (data.data[x].is_valid == 1) {
              this.roleData.push({
                label: data.data[x].name,
                value: data.data[x].id
              });
            }
          }
        }
      });
    },
    checkPass() {
      if (
        this.password === "" ||
        this.password === undefined ||
        this.password.length == 0
      ) {
        this.$notify.error({
          message: "请填写密码",
          type: "error"
        });
      } else {
        var para = {
          login_name: this.login_name
        };
        userLoginGetSalt(para).then(data => {
          if (data["code"] !== 200) {
            this.$message({
              message: data["msg"],
              type: "error"
            });
          } else {
            var para = {
              login_name: this.login_name,
              password: this.md5It(
                this.md5It(this.md5It(this.password) + data.data.stable_salt) +
                  data.data.salt
              ),
              is_generate_cookie: false
            };
            userLogin(para).then(data2 => {
              if (data2["code"] !== 200) {
                this.$message({
                  message: data2.msg,
                  type: "error"
                });
              } else {
                this.$message({
                  message: data2.msg,
                  type: "success"
                });
                this.isCheckedPass = true;
              }
            });
          }
        });
      }
    },
    changePass() {
      var stable_salt = this.randomString(40);
      var para = {
        login_name: this.login_name,
        stable_salt: stable_salt,
        password: this.md5It(this.md5It(this.passwordNew) + stable_salt)
      };
      userChangePassword(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.$message({
            message: data["msg"],
            type: "success"
          });
          this.passwordNew = "";
        }
      });
    },
    changeRole() {
      var para = {
        role_id: this.role_id,
        login_name: this.login_name
      };
      userRoleChange(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.$message({
            message: data["msg"],
            type: "success"
          });
          this.passwordNew = "";
        }
      });
    },
    userAddFront() {
      if (
        this.userNameNew === "" ||
        this.userNameNew === undefined ||
        this.userNameNew.length == 0 ||
        this.passwordNew === "" ||
        this.passwordNew === undefined ||
        this.passwordNew.length == 0 ||
        this.role_id == ""
      ) {
        this.$notify.error({
          message: "请将表单填写完整后提交",
          type: "error"
        });
      } else {
        var stable_salt = this.randomString(40);
        var para = {
          name: this.userNameNew,
          role_id: this.role_id,
          login_name: this.login_name,
          stable_salt: stable_salt,
          password: this.md5It(this.md5It(this.passwordNew) + stable_salt)
        };
        userAdd(para).then(data => {
          if (data["code"] !== 200) {
            this.$message({
              message: data["msg"],
              type: "error"
            });
          } else {
            this.$message({
              message: data["msg"],
              type: "success"
            });
            this.passwordNew = "";
          }
        });
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
.div-flex {
  display: flex;
}
.main_input--large {
  width: 350px;
}
.main_input--medium {
  width: 200px;
}
.main_input--small {
  width: 100px;
}
.main_input--tiny {
  width: 100px;
}
.width--large {
  width: 350px;
}
.width--medium {
  width: 200px;
}
.width--small {
  width: 100px;
}
.inline_margin--small {
  margin-left: 10px;
}
.inline_margin--medium {
  margin-left: 20px;
}
.inline_margin--large {
  margin-left: 20px;
}
.min_height-medium {
  min-height: 150px;
}
.td--label {
  max-width: 200px;
  min-width: 140px;
}
.td--label--medium {
  min-width: 100px;
}
.td--label--short {
  min-width: 40px;
}
.td__p--label {
  font-weight: bold;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
}
.padding_right-small {
  padding-right: 8px;
}
.padding_left-small {
  padding-left: 8px;
}
.min_width-small {
  min-width: 10px;
}
.collapse-div {
  color: rgb(96, 98, 102);
  font-size: 12px;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
}
.info-text {
  color: rgb(96, 98, 102);
  font-size: 30px;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 100px;
}
.right-side-box-card {
  min-height: 500px;
}
.left-side-box-card {
  min-height: 500px;
}
.el-icon-back {
  font-size: 180px;
}
.single-data-setting {
  position: absolute;
  right: 0px;
  top: 0px;
  z-index: 99;
  margin-right: 20px;
}
.add {
  margin-top: 10px;
  width: 100%;
  height: 34px;
  border: 1px dashed #c1c1cd;
  border-radius: 3px;
  cursor: pointer;
  justify-content: center;
  display: flex;
  line-height: 34px;
  color: rgb(96, 98, 102);
}
.dialog-type-tooltip {
  padding-left: 3px;
  padding-right: 30px;
}
.edit-form-question-mark {
  padding-left: 5px;
}
.noMargin {
  margin-left: 0px;
  margin-top: 0px;
  margin-right: 0px;
  margin-bottom: 0px;
}
.padding-right-19 {
  padding-right: 19px;
}
.scrollbar-div {
  width: 100%;
  overflow-x: hidden;
  overflow-y: overlay;
}
.scrollbar-div::-webkit-scrollbar {
  width: 5px;
  height: 1px;
}
.scrollbar-div::-webkit-scrollbar-thumb {
  border-radius: 10px;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  background: rgba(83, 83, 83, 0.18);
}
.scrollbar-div::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.13);
  border-radius: 10px;
  background: #f3f3f300;
}
.max-height-large {
  max-height: 70vh;
}
.max-height-medium {
  max-height: 40vh;
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
.margin_left-large {
  margin-left: 40px;
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
.margin-medium {
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-right: 20px;
}
.scrollbar-div {
  max-height: 80vh;
  width: 100%;
  overflow-x: hidden;
  overflow-y: overlay;
}
.scrollbar-div::-webkit-scrollbar {
  width: 3px;
  height: 1px;
}
.scrollbar-div::-webkit-scrollbar-thumb {
  border-radius: 10px;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  background: rgba(83, 83, 83, 0.18);
}
.scrollbar-div::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.13);
  border-radius: 10px;
  background: #f3f3f300;
}
.dialog-footer {
  margin: 20px 20px 20px 20px;
  position: absolute;
  bottom: 0;
  right: 0;
  z-index: 99;
}
</style>