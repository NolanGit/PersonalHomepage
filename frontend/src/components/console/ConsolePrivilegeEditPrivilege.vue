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
import { privilegeEdit } from "../../api/privilege";
export default {
  name: "ConsolePrivilegeEditPrivilege",
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
    submit() {
      if (this.action == "new") {
        var para = {
          privilege_id: this.privilegeId,
          name: this.privilegeName,
          mark: this.privilegeMark,
          remark: this.privilegeRemark
        };
        privilegeEdit(para).then(data => {
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
            this.$emit("close");
          }
        });
      }
    }
  },
  mounted() {}
};
</script>

<style scoped>
.div-flex {
  display: flex;
}
.width--medium {
  width: 200px;
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
::-webkit-scrollbar {
  width: 5px;
  height: 1px;
}
::-webkit-scrollbar-thumb {
  border-radius: 10px;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  background: rgba(83, 83, 83, 0.18);
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