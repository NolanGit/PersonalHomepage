<template>
  <section>
    <el-row class="main-row" :gutter="20">
      <div class="margin_left-large">
        <el-checkbox-group class="margin_bottom-large" v-model="checkedPrivilege">
          <el-checkbox
            v-for="singlePrivilegeData in privilegeData"
            :key="singlePrivilegeData"
            :label="singlePrivilegeData.label"
            :value="singlePrivilegeData.id"
          ></el-checkbox>
        </el-checkbox-group>
        <el-button class="noMargin" size="mini" plain type="primary" @click="submit()">确定</el-button>
      </div>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
import rolePrivilegeEdit from "../../api/console";
export default {
  name: "ConsolePrivilegeEditRolePrivilege",
  props: {
    roleId: Number,
    privilegeData: Array,
    checkedPrivilege: Array
  },
  watch: {
    privilegeData(newVal, oldVal) {
      this.privilegeData = newVal;
      console.log(newVal);
    },
    checkedPrivilege(newVal, oldVal) {
      this.checkedPrivilege = newVal;
      console.log(newVal);
    }
  },
  data() {
    return {
      checkedPrivilegeId: []
    };
  },
  methods: {
    submit() {
      this.checkedPrivilegeId = [];
      for (let x = 0; x < this.privilegeData.length; x++) {
        for (let y = 0; y < this.checkedPrivilege.length; y++) {
          if (this.privilegeData[x].label == this.checkedPrivilege[y]) {
            this.checkedPrivilegeId.push(this.privilegeData[x].id);
            continue;
          }
        }
      }
      var para = {
        role_id: this.roleId,
        checked_privilege_id=this.checkedPrivilegeId
      };
      rolePrivilegeEdit(para).then(data => {
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
        }
      });

    }
  },
  mounted() {}
};
</script>

<style scoped>
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
.margin_left-large {
  margin-left: 40px;
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