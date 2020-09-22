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
            <!-- 如果不加:key，vue会试图复用原有的组件，会产生问题 详情参见vue中:key的作用 -->
            <el-table
              :key="Math.random()"
              size="mini"
              height="400"
              :data="userData"
              stripe
              style="width: 100%"
              ref="userTable"
            >
              <!-- <el-table-column :key="Math.random()" prop="id" sortable label="ID" width="70"></el-table-column> -->
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
                    @click="userDisable(scope.row.id)"
                  >禁用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="userEnable(scope.row.id)"
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
                    @click="userDelete(scope.row.id)"
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
              <!-- <el-table-column :key="Math.random()" prop="id" sortable label="ID" width="70"></el-table-column> -->
              <el-table-column :key="Math.random()" prop="name" label="名称" width="180"></el-table-column>
              <el-table-column :key="Math.random()" prop="remark" label="备注" width="180"></el-table-column>
              <el-table-column :key="Math.random()" prop="is_disabled" label="是否禁用" width="80"></el-table-column>
              <el-table-column :key="Math.random()" prop="update_time" label="修改时间" width="180"></el-table-column>
              <el-table-column :key="Math.random()" label="操作">
                <template slot-scope="scope">
                  <el-button
                    v-show="scope.row.is_valid==1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="danger"
                    @click="roleDisable(scope.row.id)"
                  >禁用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="roleEnable(scope.row.id)"
                  >启用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="roleEdit(scope.row.id,scope.row.name,scope.row.remark)"
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
                    @click="roleDelete(scope.row.id)"
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
              <!-- <el-table-column :key="Math.random()" prop="id" sortable label="ID" width="70"></el-table-column> -->
              <el-table-column :key="Math.random()" prop="name" sortable label="名称" width="220"></el-table-column>
              <el-table-column :key="Math.random()" prop="mark" sortable label="标识" width="200"></el-table-column>
              <el-table-column :key="Math.random()" prop="remark" label="备注" width="170"></el-table-column>
              <el-table-column :key="Math.random()" prop="is_disabled" label="是否禁用" width="70"></el-table-column>
              <el-table-column :key="Math.random()" prop="update_time" sortable label="修改时间"></el-table-column>
              <el-table-column :key="Math.random()" label="操作">
                <template slot-scope="scope">
                  <el-button
                    v-show="scope.row.is_valid==1"
                    class="noMargin"
                    size="mini"
                    plain
                    type="danger"
                    @click="privilegeDisable(scope.row.id)"
                  >禁用</el-button>
                  <el-button
                    v-show="scope.row.is_valid==0"
                    class="noMargin"
                    size="mini"
                    plain
                    type="primary"
                    @click="privilegeEnable(scope.row.id)"
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
        size="60%"
        @closed="editFormClosed"
        direction="btt"
      >
        <div v-if="edit.type=='user' & edit.visible">
          <PrivilegeEditUser
            :user_id="user_id"
            :login_name="edit.login_name"
            :action="edit.userEditAction"
            @close="close()"
          />
        </div>
        <div v-if="edit.type=='role' & edit.visible">
          <PrivilegeEditRole
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
          <PrivilegeEditPrivilege
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
import PrivilegeEditUser from "./PrivilegeEditUser";
import PrivilegeEditRole from "./PrivilegeEditRole";
import PrivilegeEditPrivilege from "./PrivilegeEditPrivilege";
const api = {
  userGet: "/privilege/userGet",
  userDisable: "/privilege/userDisable",
  userEnable: "/privilege/userEnable",
  userDelete: "/privilege/userDelete",
  roleGet: "/privilege/roleGet",
  rolePrivilegeGet: "/privilege/rolePrivilegeGet",
  roleDisable: "/privilege/roleDisable",
  roleEnable: "/privilege/roleEnable",
  roleDelete: "/privilege/roleDelete",
  privilegeGet: "/privilege/privilegeGet",
  privilegeDisable: "/privilege/privilegeDisable",
  privilegeEnable: "/privilege/privilegeEnable",
  privilegeDelete: "/privilege/privilegeDelete"
};
export default {
  name: "ConsolePrivilege",
  components: {
    PrivilegeEditUser,
    PrivilegeEditRole,
    PrivilegeEditPrivilege
  },
  props: {
    user_id: Number,
    login_name: String
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
        this.userData = [];
        this.userGet();
      } else if (this.activeSystem == "角色对应权限设置") {
        this.roleData = [];
        this.roleGet();
      } else if (this.activeSystem == "权限设置") {
        this.privilegeData = [];
        this.privilegeGet();
      }
    },
    //各组件编辑窗口关闭后回调
    close() {
      this.edit.visible = false;
      if (this.edit.type == "user") {
        this.userGet();
      }
      if (this.edit.type == "role") {
        this.roleGet();
      }
      if (this.edit.type == "privilege") {
        this.privilegeGet();
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
    //修改用户信息
    userSetting(row_login_name) {
      this.edit.login_name = row_login_name;
      this.edit.title = "修改用户密码和角色";
      this.edit.visible = true;
      this.edit.type = "user";
      this.edit.userEditAction = "edit";
    },
    async userGet() {
      try {
        const { data: res } = await axios.post(api.userGet, {
          user_id: this.user_id
        });
        for (let x = 0; x < res.data.length; x++) {
          if (res.data[x].is_valid == 1) {
            res.data[x].is_disabled = "否";
          } else if (res.data[x].is_valid == 0) {
            res.data[x].is_disabled = "是";
          }
        }
        this.userData = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //用户禁用
    async userDisable(user_id) {
      try {
        const { data: res } = await axios.post(api.userDisable, {
          user_id: user_id
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.userGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //用户启用
    async userEnable(user_id) {
      try {
        const { data: res } = await axios.post(api.userEnable, {
          user_id: user_id
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.userGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //用户删除
    async userDelete(user_id) {
      this.$confirm("确认删除吗?", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.userDelete, {
            user_id: user_id
          });
          this.$message({
            message: res["msg"],
            type: "success"
          });
          this.userGet();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      });
    },

    // 【以下为角色相关方法】
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
    //角色编辑
    roleEdit(role_id, role_name, role_remark) {
      this.edit.roleEditAction = "new";
      this.edit.roleEditRoleId = role_id;
      this.edit.roleEditName = role_name;
      this.edit.roleEditRemark = role_remark;
      this.edit.title = "修改角色";
      this.edit.visible = true;
      this.edit.type = "role";
    },
    //角色获取数据
    async roleGet() {
      try {
        const { data: res } = await axios.get(api.roleGet);
        for (let x = 0; x < res.data.length; x++) {
          if (res.data[x].is_valid == 1) {
            res.data[x].is_disabled = "否";
          } else if (res.data[x].is_valid == 0) {
            res.data[x].is_disabled = "是";
          }
        }
        this.roleData = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //角色修改对应权限
    async roleSetting(role_id) {
      try {
        const { data: res } = await axios.post(api.rolePrivilegeGet, {
          role_id: role_id
        });
        this.edit.checkedPrivilege = [];
        for (let x = 0; x < res.data.length; x++) {
          this.edit.checkedPrivilege.push(res.data[x].privilege_name);
        }
        const { data: res2 } = await axios.get(api.privilegeGet);
        this.edit.privilegeData = [];
        for (let x = 0; x < res2.data.length; x++) {
          this.edit.privilegeData.push({
            id: res2.data[x].id,
            label: res2.data[x].name
          });
        }
        this.edit.roleEditRoleId = role_id;
        this.edit.roleEditAction = "edit";
        this.edit.title = "修改角色对应权限";
        this.edit.type = "role";
        this.edit.visible = true;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //角色禁用
    async roleDisable(role_id) {
      try {
        const { data: res } = await axios.post(api.roleDisable, {
          role_id: role_id
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.roleGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //角色启用
    async roleEnable(role_id) {
      try {
        const { data: res } = await axios.post(api.roleEnable, {
          role_id: role_id
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.roleGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //角色删除
    async roleDelete(role_id) {
      this.$confirm("确认删除吗?", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.userDelete, {
            role_id: role_id
          });
          this.$message({
            message: res["msg"],
            type: "success"
          });
          this.roleGet();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      });
    },

    // 【以下为权限相关方法】
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
    //权限获取数据
    async privilegeGet() {
      try {
        const { data: res } = await axios.get(api.privilegeGet);
        this.privilegeData = [];
        for (let x = 0; x < res.data.length; x++) {
          this.privilegeData.push({
            id: res.data[x].id,
            label: res.data[x].name,
            name: res.data[x].name,
            mark: res.data[x].mark,
            remark: res.data[x].remark,
            is_valid: res.data[x].is_valid,
            update_time: res.data[x].update_time,
            is_disabled: res.data[x].is_valid == 1 ? "否" : "是"
          });
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //权限禁用
    async privilegeDisable(privilege_id) {
      try {
        const { data: res } = await axios.post(api.privilegeDisable, {
          privilege_id: privilege_id
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.privilegeGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //权限启用
    async privilegeEnable(privilege_id) {
      try {
        const { data: res } = await axios.post(api.privilegeEnable, {
          privilege_id: privilege_id
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.privilegeGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    //权限删除
    async privilegeDelete(privilege_id) {
      this.$confirm("确认删除吗?", "提示", {}).then(async () => {
        try {
          const { data: res } = await axios.post(api.privilegeDelete, {
            privilege_id: privilege_id
          });
          this.$message({
            message: res["msg"],
            type: "success"
          });
          this.privilegeGet();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      });
    }
  },
  mounted() {
    this.userGet();
  }
};
</script>

<style scoped>
.noMargin {
  margin: 0;
}
</style>