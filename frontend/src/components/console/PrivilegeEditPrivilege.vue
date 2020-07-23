<template>
  <section>
    <el-row class="main-row" :gutter="20">
      <div class="margin_left-large">
        <div v-if="action=='new'">
          <div class="div-flex margin_bottom-medium">
            <div class="td__p--label td--label">请输入权限名称：</div>
            <el-input
              class="width--medium margin_right-small"
              v-model="privilegeName"
              size="small"
              placeholder="请输入"
            ></el-input>
          </div>
          <div class="div-flex margin_bottom-medium">
            <div class="td__p--label td--label">请输入权限标识：</div>
            <el-input
              class="width--medium margin_right-small"
              v-model="privilegeMark"
              size="small"
              placeholder="请输入"
            ></el-input>
          </div>
          <div class="div-flex margin_bottom-medium">
            <div class="td__p--label td--label">请输入备注：</div>
            <el-input
              class="width--medium margin_right-small"
              v-model="privilegeRemark"
              size="small"
              placeholder="请输入"
            ></el-input>
          </div>
        </div>
        <el-button class="noMargin" size="mini" plain type="primary" @click="submit()">确定</el-button>
      </div>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
const api = {
  privilegeEdit: "/privilege/privilegeEdit"
};
export default {
  name: "PrivilegeEditPrivilege",
  props: {
    action: String, // action=='new':新增角色页面
    privilegeId: Number,
    privilegeName: String,
    privilegeMark: String,
    privilegeRemark: String
  },
  watch: {
    privilegeId(newVal, oldVal) {
      this.privilegeId = newVal;
    }
  },
  data() {
    return {};
  },
  methods: {
    async submit() {
      if (this.action == "new") {
        try {
          const { data: res } = await axios.post(api.privilegeEdit, {
            privilege_id: this.privilegeId,
            name: this.privilegeName,
            mark: this.privilegeMark,
            remark: this.privilegeRemark
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
  mounted() {}
};
</script>

<style scoped>
</style>