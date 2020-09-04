<template>
  <section class="scrollbar-div" style="max-height: 50vh;">
    <el-row class="main-row" :gutter="20">
      <div class="margin_left-large">
        <div v-if="action=='edit'">
          <el-checkbox-group class="margin_bottom-large" v-model="checkedPrivilege">
            <el-checkbox
              v-for="singlePrivilegeData in privilegeData"
              :key="singlePrivilegeData"
              :label="singlePrivilegeData.label"
              :value="singlePrivilegeData.id"
              style="min-width: 300px;"
            ></el-checkbox>
          </el-checkbox-group>
        </div>
        <div v-if="action=='new'">
          <div class="div-flex margin_bottom-medium">
            <div class="td__p--label td--label">请输入角色名称：</div>
            <el-input
              class="width--medium margin_right-small"
              v-model="roleName"
              size="small"
              placeholder="请输入"
            ></el-input>
          </div>
          <div class="div-flex margin_bottom-medium">
            <div class="td__p--label td--label">请输入备注：</div>
            <el-input
              class="width--medium margin_right-small"
              v-model="roleRemark"
              size="small"
              placeholder="请输入"
            ></el-input>
          </div>
        </div>
        <el-button class="noMargin" size="mini" plain type="primary" @click="submit()" style="margin-bottom: 50px;">确定</el-button>
      </div>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
const api = {
  rolePrivilegeEdit: "/privilege/rolePrivilegeEdit",
  roleEdit: "/privilege/roleEdit"
};
export default {
  name: "PrivilegeEditRole",
  props: {
    action: String, // action=='edit':加载编辑角色和权限对应关系页面; action=='new':新增角色页面
    roleId: Number,
    roleName: String,
    roleRemark: String,
    privilegeData: Array,
    checkedPrivilege: Array
  },
  watch: {
    privilegeData(newVal, oldVal) {
      this.privilegeData = newVal;
    },
    checkedPrivilege(newVal, oldVal) {
      this.checkedPrivilege = newVal;
    },
    roleId(newVal, oldVal) {
      this.roleId = newVal;
    },
    roleName(newVal, oldVal) {
      this.roleName = newVal;
    },
    roleRemark(newVal, oldVal) {
      this.roleRemark = newVal;
    }
  },
  data() {
    return {};
  },
  methods: {
    async submit() {
      if (this.action == "edit") {
        this.checkedPrivilegeId = [];
        for (let x = 0; x < this.privilegeData.length; x++) {
          for (let y = 0; y < this.checkedPrivilege.length; y++) {
            if (this.privilegeData[x].label == this.checkedPrivilege[y]) {
              this.checkedPrivilegeId.push(this.privilegeData[x].id);
              continue;
            }
          }
        }
        try {
          const { data: res } = await axios.post(api.rolePrivilegeEdit, {
            role_id: this.roleId,
            checked_privilege_id: this.checkedPrivilegeId
          });
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
      } else if (this.action == "new") {
        try {
          const { data: res } = await axios.post(api.roleEdit, {
            role_id: this.roleId,
            name: this.roleName,
            remark: this.roleRemark
          });
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
    console.log(this.checkedPrivilege);
  }
};
</script>

<style scoped>
</style>