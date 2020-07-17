<template>
  <el-card class="left-side-box-card">
    <el-collapse v-model="activeSystem" accordion>
      <el-collapse-item
        v-for="singleSystem in subSystem"
        :key="singleSystem.key"
        :title="singleSystem.title"
        :name="singleSystem.title"
      >
        <div
          class="collapse-div"
          v-show="singleSystem.scriptText!=''"
        >包括：{{singleSystem.scriptText}}</div>
        <div class="collapse-div" v-show="formData.length==0">本栏目暂无脚本</div>
        <el-button type="text" v-show="formData.length==0" size="small" @click="newTab">需要新增？</el-button>
        <el-button class="noMargin" type="text" size="small" @click="subSystemDelete()">删除栏目</el-button>
      </el-collapse-item>
    </el-collapse>
    <el-popover placement="right" trigger="hover">
      <el-input size="mini" style="width: 170px" placeholder="请输入栏目名称" v-model="subSystemName"></el-input>
      <el-button class="margin_top-mini" size="mini" @click="subSystemAdd">确定</el-button>
      <el-button slot="reference" class="margin_top-medium" type="text" size="small">新增栏目</el-button>
    </el-popover>
  </el-card>
</template>

<script>
import axios from "axios";
import { deepClone } from "../../js/common";
const api = {
  subSystem: "/script/subSystem",
  subSystemAdd: "/script/subSystemAdd",
  subSystemDelete: "/script/subSystemDelete"
};
export default {
  data() {
    return {
      activeSystem: [],
      subSystem: [],
      subSystemName: ""
    };
  },
  watch: {
    activeSystem(newVal, oldVal) {
      if (newVal == "") {
        return;
      }
      for (var s = 0; s < this.subSystem.length; s++) {
        if (newVal == this.subSystem[s].title) {
          break;
        }
      }
      this.$emit(this.subSystem[s].id);
    }
  },
  methods: {
    //删除栏目
    async subSystemDelete() {
      this.$confirm("确认删除吗?", "提示", {}).then(async () => {
        try {
          for (var s = 0; s < this.subSystem.length; s++) {
            if (this.activeSystem == this.subSystem[s].title) {
              break;
            }
          }
          const { data: res } = await axios.post(api.subSystemDelete, {
            sub_system_id: this.subSystem[s].id,
            user_id: this.user_id
          });
          this.$message({
            message: "成功！",
            type: "success"
          });
          this.getSubSystem();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      });
    },
    //添加栏目
    async subSystemAdd() {
      try {
        const { data: res } = await axios.post(api.subSystemAdd, {
          sub_system_name: this.subSystemName,
          user_id: this.user_id
        });
        this.subSystem = [];
        this.subSystemScript();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    }
  }
};
</script>

<style>
</style>