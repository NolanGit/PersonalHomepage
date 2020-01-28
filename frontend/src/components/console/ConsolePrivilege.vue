<template>
  <section>
    <el-row class="main-row margin_bottom-medium" :gutter="20">
      <el-col :span="5" class="lift-side-bar">
        <el-card class="left-side-box-card">
          <el-collapse v-model="activeSystem" @change="handleChange" accordion>
            <el-collapse-item title="用户设置" name="用户设置">
              <div class="collapse-div">包括用户密码、角色的修改</div>
            </el-collapse-item>
            <el-collapse-item title="角色对应权限设置" name="角色对应权限设置">
              <div class="collapse-div">包括角色的新增、角色对应权限的设置</div>
            </el-collapse-item>
            <el-collapse-item title="权限设置" name="权限设置">
              <div class="collapse-div">包括权限的新增、修改和删除</div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-col>
      <el-col :span="19" class="right-side-bar">
        <el-card class="left-side-box-card">
          <div v-if="activeSystem=='用户设置'">
            <el-button size="small" type="primary" @click="userAdd()">新增用户</el-button>
            <el-table :data="userData" stripe style="width: 100%">
              <el-table-column prop="id" label="ID" width="180"></el-table-column>
              <el-table-column prop="login_name" label="登录名" width="180"></el-table-column>
              <el-table-column prop="name" label="姓名" width="180"></el-table-column>
              <el-table-column prop="role_name" label="角色" width="180"></el-table-column>
              <el-table-column prop="update_time" label="修改时间"></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button
                    v-if="scope.row.is_edit==1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="userSetting(scope.row.login_name)"
                  >修改</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div v-if="activeSystem=='角色对应权限设置'">
            <el-button size="small" type="primary" @click="roleAdd()">新增角色</el-button>
            <el-table :data="roleData" stripe style="width: 100%">
              <el-table-column prop="id" label="ID" width="180"></el-table-column>
              <el-table-column prop="name" label="名称" width="180"></el-table-column>
              <el-table-column prop="remark" label="备注" width="180"></el-table-column>
              <el-table-column prop="is_disabled" label="是否禁用" width="180"></el-table-column>
              <el-table-column prop="create_time" label="修改时间"></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="roleSetting(scope.row.id)"
                  >配置对应权限</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div v-if="activeSystem=='权限设置'">
            <el-button size="small" type="primary" @click="privilegeAdd()">新增权限</el-button>
            <el-table :data="privilegeData" stripe style="width: 100%">
              <el-table-column prop="id" label="ID" width="80"></el-table-column>
              <el-table-column prop="name" label="名称" width="200"></el-table-column>
              <el-table-column prop="mark" label="标识" width="230"></el-table-column>
              <el-table-column prop="remark" label="备注" width="200"></el-table-column>
              <el-table-column prop="is_disabled" label="是否禁用" width="80"></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="privilegeEdit(scope.row.id)"
                  >修改</el-button>
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="privilegeDisable(scope.row.id)"
                  >禁用</el-button>
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="privilegeDelete(scope.row.id)"
                  >删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
      <el-drawer
        :title="edit.title"
        :visible.sync="edit.visible"
        :close-on-click-modal="false"
        size="60%"
        @closed="editFormClosed"
        direction="btt"
      >
        <div v-if="edit.type=='user' & edit.visible">
          <ConsolePrivilegeEditUser :login_name="edit.login_name" />
        </div>
        <div v-if="edit.type=='rolePrivilege' & edit.visible">
          <ConsolePrivilegeEditRolePrivilege
            :checkedPrivilege="edit.checkedPrivilege"
            :privilegeData="edit.privilegeData"
          />
        </div>
        <div v-if="edit.type=='privilege' & edit.visible">
          <ConsolePrivilegeEditRolePrivilege
            :checkedPrivilege="edit.checkedPrivilege"
            :privilegeData="edit.privilegeData"
          />
        </div>
      </el-drawer>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
import {
  userGet,
  roleGet,
  privilegeGet,
  rolePrivilegeGet
} from "../../api/console";
import ConsolePrivilegeEditRolePrivilege from "./ConsolePrivilegeEditRolePrivilege";
import ConsolePrivilegeEditUser from "./ConsolePrivilegeEditUser";
export default {
  name: "ConsolePrivilege",
  components: {
    ConsolePrivilegeEditUser,
    ConsolePrivilegeEditRolePrivilege
  },
  data() {
    return {
      activeSystem: "用户设置",
      userData: [],
      roleData: [],
      privilegeData: [],
      edit: {
        title: "编辑",
        visible: false,
        type: ""
      }
    };
  },
  methods: {
    handleChange() {
      if (this.activeSystem == "用户设置") {
        this.userGetFront();
      } else if (this.activeSystem == "角色对应权限设置") {
        this.roleGetFront();
      } else if (this.activeSystem == "权限设置") {
        this.privilegeGetFront();
      }
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
              data.data[x].is_disabled = "否";
            } else if (data.data[x].is_valid == 0) {
              data.data[x].is_disabled = "是";
            }
          }
          this.roleData = data.data;
        }
      });
    },
    privilegeGetFront() {
      privilegeGet().then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.privilegeData = [];
          for (let x = 0; x < data.data.length; x++) {
            this.privilegeData.push({
              id: data.data[x].id,
              label: data.data[x].name,
              name: data.data[x].name,
              mark: data.data[x].mark,
              remark: data.data[x].remark,
              is_valid: data.data[x].is_valid,
              update_time: data.data[x].update_time,
              is_disabled: data.data[x].is_valid == 1 ? "否" : "是"
            });
          }
        }
      });
    },
    roleSetting(role_id) {
      var para = {
        role_id: role_id
      };
      rolePrivilegeGet(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.edit.checkedPrivilege = [];
          for (let x = 0; x < data.data.length; x++) {
            this.edit.checkedPrivilege.push(data.data[x].privilege_name);
          }
          privilegeGet().then(data => {
            if (data["code"] !== 200) {
              this.$message({
                message: data["msg"],
                type: "error"
              });
            } else {
              this.edit.privilegeData = [];
              for (let x = 0; x < data.data.length; x++) {
                this.edit.privilegeData.push({
                  id: data.data[x].id,
                  label: data.data[x].name
                });
              }
              this.edit.title = "修改角色对应权限";
              this.edit.visible = true;
              this.edit.type = "rolePrivilege";
            }
          });
        }
      });
    },
    userSetting(login_name) {
      this.edit.title = "修改用户密码和角色";
      this.edit.visible = true;
      this.edit.type = "user";
      this.edit.login_name = login_name;
    }
  },
  mounted() {
    this.userGetFront();
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
.main_select--large {
  width: 350px;
}
.main_select--medium {
  width: 200px;
}
.main_select--small {
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
.output-html {
  font-family: PingFang SC;
}
.output-div {
  height: 45vh;
  width: 100%;
  overflow-x: hidden;
  overflow-y: hidden;
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
.edit-form-card {
  padding-bottom: 10px;
}
.singleDataOptionDialogValue {
  padding-left: 30px;
}
.singleDataOptionDialogDeleted {
  padding-left: 8px;
}
.editFormRightButtons {
  padding-left: 20px;
}
.editFormRightButton {
  font-size: 25px;
}
.editFormMoveUp {
  padding-right: 8px;
}
.editFormMoveDown {
  padding-right: 8px;
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