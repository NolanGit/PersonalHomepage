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
            <el-button
              size="mini"
              class="margin_bottom-small"
              type="primary"
              @click="userAdd()"
            >新增用户</el-button>
            <el-table
              :key="Math.random()"
              size="mini"
              height="400"
              :data="userData"
              stripe
              style="width: 100%"
              ref="userTable"
            >
              <el-table-column :key="Math.random()" prop="id" sortable label="ID" width="80"></el-table-column>
              <el-table-column :key="Math.random()" prop="name" label="姓名" width="120"></el-table-column>
              <el-table-column :key="Math.random()" prop="login_name" label="登录名" width="180"></el-table-column>
              <el-table-column :key="Math.random()" prop="role_name" label="角色" width="120"></el-table-column>
              <el-table-column :key="Math.random()" prop="is_disabled" label="是否禁用" width="80"></el-table-column>
              <el-table-column :key="Math.random()" prop="update_time" label="修改时间"></el-table-column>
              <el-table-column :key="Math.random()" label="操作">
                <template slot-scope="scope">
                  <el-button
                    v-show="scope.row.is_valid==1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="danger"
                    @click="userDisableFront(scope.row.id)"
                  >禁用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="userEnableFront(scope.row.id)"
                  >启用</el-button>
                  <el-button
                    v-if="scope.row.is_edit==1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="userSetting(scope.row.login_name)"
                  >修改</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    type="danger"
                    @click="userDeleteFront(scope.row.id)"
                  >删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div v-if="activeSystem=='角色对应权限设置'">
            <el-button
              size="mini"
              class="margin_bottom-small"
              type="primary"
              @click="roleAdd()"
            >新增角色</el-button>
            <el-table
              :key="Math.random()"
              size="mini"
              height="400"
              :data="roleData"
              stripe
              style="width: 100%"
              ref="roleTable"
            >
              <el-table-column :key="Math.random()" prop="id" sortable label="ID" width="80"></el-table-column>
              <el-table-column :key="Math.random()" prop="name" label="名称" width="180"></el-table-column>
              <el-table-column :key="Math.random()" prop="remark" label="备注" width="180"></el-table-column>
              <el-table-column :key="Math.random()" prop="is_disabled" label="是否禁用" width="80"></el-table-column>
              <el-table-column :key="Math.random()" prop="update_time" label="修改时间"></el-table-column>
              <el-table-column :key="Math.random()" label="操作">
                <template slot-scope="scope">
                  <el-button
                    v-show="scope.row.is_valid==1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="danger"
                    @click="roleDisableFront(scope.row.id)"
                  >禁用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="roleEnableFront(scope.row.id)"
                  >启用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="roleEditFront(scope.row.id,scope.row.name,scope.row.remark)"
                  >修改</el-button>
                  <el-button
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="roleSetting(scope.row.id)"
                  >配置对应权限</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    type="danger"
                    @click="roleDeleteFront(scope.row.id)"
                  >删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div v-if="activeSystem=='权限设置'">
            <el-button
              size="mini"
              class="margin_bottom-small"
              type="primary"
              @click="privilegeAdd()"
            >新增权限</el-button>
            <el-table
              :key="Math.random()"
              size="mini"
              height="400"
              :data="privilegeData"
              stripe
              style="width: 100%"
              ref="privilegeTable"
            >
              <el-table-column :key="Math.random()" prop="id" sortable label="ID" width="80"></el-table-column>
              <el-table-column :key="Math.random()" prop="name" sortable label="名称" width="200"></el-table-column>
              <el-table-column :key="Math.random()" prop="mark" sortable label="标识" width="230"></el-table-column>
              <el-table-column :key="Math.random()" prop="remark" label="备注" width="300"></el-table-column>
              <el-table-column :key="Math.random()" prop="is_disabled" label="是否禁用" width="80"></el-table-column>
              <el-table-column :key="Math.random()" prop="update_time" label="修改时间"></el-table-column>
              <el-table-column :key="Math.random()" label="操作">
                <template slot-scope="scope">
                  <el-button
                    v-show="scope.row.is_valid==1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="danger"
                    @click="privilegeDisableFront(scope.row.id)"
                  >禁用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="privilegeEnableFront(scope.row.id)"
                  >启用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="privilegeEditFront(scope.row.id,scope.row.name,scope.row.mark,scope.row.remark)"
                  >修改</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    type="danger"
                    @click="privilegeDeleteFront(scope.row.id)"
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
          <ConsolePrivilegeEditUser
            :login_name="edit.login_name"
            :action="edit.userEditAction"
            @close="close()"
          />
        </div>
        <div v-if="edit.type=='role' & edit.visible">
          <ConsolePrivilegeEditRole
            :action="edit.roleEditAction"
            :checkedPrivilege="edit.checkedPrivilege"
            :privilegeData="edit.privilegeData"
            :roleId="edit.roleEditRoleId"
            :roleName="edit.roleEditName"
            :roleRemark="edit.roleEditRemark"
            @close="close()"
          />
        </div>
        <div v-if="edit.type=='privilege' & edit.visible">
          <ConsolePrivilegeEditPrivilege
            :action="edit.privilegeEditAction"
            :privilegeId="edit.privilegeEditPrivilegeId"
            :privilegeName="edit.privilegeEditPrivilegeName"
            :privilegeMark="edit.privilegeEditPrivilegeMark"
            :privilegeRemark="edit.privilegeEditPrivilegeRemark"
            @close="close()"
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
  userDisable,
  userEnable,
  userDelete,
  roleGet,
  rolePrivilegeGet,
  roleDisable,
  roleEnable,
  roleDelete,
  privilegeGet,
  privilegeDisable,
  privilegeEnable,
  privilegeDelete
} from "../../api/privilege";
import ConsolePrivilegeEditUser from "./ConsolePrivilegeEditUser";
import ConsolePrivilegeEditRole from "./ConsolePrivilegeEditRole";
import ConsolePrivilegeEditPrivilege from "./ConsolePrivilegeEditPrivilege";
export default {
  name: "ConsolePrivilege",
  components: {
    ConsolePrivilegeEditUser,
    ConsolePrivilegeEditRole,
    ConsolePrivilegeEditPrivilege
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
    //切换handle
    handleChange() {
      if (this.activeSystem == "用户设置") {
        this.userGetFront();
      } else if (this.activeSystem == "角色对应权限设置") {
        this.roleGetFront();
      } else if (this.activeSystem == "权限设置") {
        this.privilegeGetFront();
      }
    },
    //各组件编辑窗口关闭后回调
    close() {
      this.edit.visible = false;
      if (this.edit.type == "user") {
        this.userGetFront();
      }
      if (this.edit.type == "role") {
        this.roleGetFront();
      }
      if (this.edit.type == "privilege") {
        this.privilegeGetFront();
      }
    },

    // 【以下为用户相关方法】
    //获取数据
    userAdd() {
      this.edit.title = "新增用户";
      this.edit.visible = true;
      this.edit.type = "user";
      this.edit.userEditAction = "new";
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
          for (let x = 0; x < data.data.length; x++) {
            if (data.data[x].is_valid == 1) {
              data.data[x].is_disabled = "否";
            } else if (data.data[x].is_valid == 0) {
              data.data[x].is_disabled = "是";
            }
          }
          this.userData = data.data;
        }
      });
    },
    //修改用户信息
    userSetting(login_name) {
      this.edit.title = "修改用户密码和角色";
      this.edit.visible = true;
      this.edit.type = "user";
      this.edit.login_name = login_name;
      this.edit.userEditAction = "edit";
    },
    //用户禁用
    async userDisableFront(user_id) {
      try {
        const { data: res } = await axios.post("/privilege/userDisable", {
          user_id: user_id
        });
        console.log(res);
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.userGetFront();
      } catch (e) {
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //用户启用
    userEnableFront(user_id) {
      var para = {
        user_id: user_id
      };
      userEnable(para).then(data => {
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
          this.userGetFront();
        }
      });
    },
    //用户删除
    userDeleteFront(user_id) {
      this.$confirm("确认删除吗?", "提示", {}).then(() => {
        var para = {
          user_id: user_id
        };
        userDelete(para).then(data => {
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
            this.userGetFront();
          }
        });
      });
    },

    // 【以下为角色相关方法】
    //角色获取数据
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
    //角色新增
    roleAdd() {
      this.edit.roleEditRoleId = 0;
      this.edit.roleEditName = "";
      this.edit.roleEditRemark = "";
      this.edit.roleEditAction = "new";
      this.edit.title = "新增角色";
      this.edit.visible = true;
      this.edit.type = "role";
    },
    //角色修改对应权限
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
              this.edit.roleEditRoleId = role_id;
              this.edit.roleEditAction = "edit";
              this.edit.title = "修改角色对应权限";
              this.edit.type = "role";
              this.edit.visible = true;
            }
          });
        }
      });
    },
    //角色禁用
    roleDisableFront(role_id) {
      var para = {
        role_id: role_id
      };
      roleDisable(para).then(data => {
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
          this.roleGetFront();
        }
      });
    },
    //角色启用
    roleEnableFront(role_id) {
      var para = {
        role_id: role_id
      };
      roleEnable(para).then(data => {
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
          this.roleGetFront();
        }
      });
    },
    //角色编辑
    roleEditFront(role_id, role_name, role_remark) {
      this.edit.roleEditAction = "new";
      this.edit.roleEditRoleId = role_id;
      this.edit.roleEditName = role_name;
      this.edit.roleEditRemark = role_remark;
      this.edit.title = "修改角色";
      this.edit.visible = true;
      this.edit.type = "role";
    },
    //角色删除
    roleDeleteFront(role_id) {
      this.$confirm("确认删除吗?", "提示", {}).then(() => {
        var para = {
          role_id: role_id
        };
        roleDelete(para).then(data => {
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
            this.roleGetFront();
          }
        });
      });
    },

    // 【以下为权限相关方法】
    //权限获取数据
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
    //权限新增
    privilegeAdd() {
      this.edit.privilegeEditAction = "new";
      this.edit.privilegeEditPrivilegeId = 0;
      this.edit.privilegeEditPrivilegeName = "";
      this.edit.privilegeEditPrivilegeMark = "";
      this.edit.privilegeEditPrivilegeRemark = "";
      this.edit.title = "新增权限";
      this.edit.visible = true;
      this.edit.type = "privilege";
    },
    //权限修改
    privilegeEditFront(
      privilegeId,
      privilegeName,
      privilegeMark,
      privilegeRemark
    ) {
      this.edit.privilegeEditAction = "new";
      this.edit.privilegeEditPrivilegeId = privilegeId;
      this.edit.privilegeEditPrivilegeName = privilegeName;
      this.edit.privilegeEditPrivilegeMark = privilegeMark;
      this.edit.privilegeEditPrivilegeRemark = privilegeRemark;
      this.edit.title = "修改权限";
      this.edit.visible = true;
      this.edit.type = "privilege";
    },
    //权限禁用
    privilegeDisableFront(privilege_id) {
      var para = {
        privilege_id: privilege_id
      };
      privilegeDisable(para).then(data => {
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
          this.privilegeGetFront();
        }
      });
    },
    //权限启用
    privilegeEnableFront(privilege_id) {
      var para = {
        privilege_id: privilege_id
      };
      privilegeEnable(para).then(data => {
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
          this.privilegeGetFront();
        }
      });
    },
    //权限删除
    privilegeDeleteFront(privilege_id) {
      this.$confirm("确认删除吗?", "提示", {}).then(() => {
        var para = {
          privilege_id: privilege_id
        };
        privilegeDelete(para).then(data => {
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
            this.privilegeGetFront();
          }
        });
      });
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
.margin_bottom-small {
  margin-bottom: 10px;
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