<template>
  <el-card class="left-side-box-card">
    <el-collapse v-model="activeSystem" accordion>
      <el-collapse-item
        v-for="singleSystem in subSystem"
        :key="singleSystem.key"
        :title="singleSystem.title"
        :name="singleSystem.title"
      >
        <a
          style="color: #606266; font-size: 12px; font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
        >包括：</a>
        <a v-for="(singleForm,singleFormIndex) in formData" :key="singleForm.key">
          <a
            style="cursor: pointer; color: #409EFF; font-size: 12px; font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
            type="text"
            size="small"
            @click="scriptLabelClicked(singleForm.id)"
          >{{singleForm.title}}</a>
          <a
            v-if="singleFormIndex!=formData.length-1"
            style="color: #606266; font-size: 12px; font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
          >、</a>
        </a>
        <a
          class="collapse-div"
          style="color: #606266; font-size: 12px; font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
          v-show="formData.length==0"
        >本栏目暂无脚本</a>
        <div>
          <el-button type="text" v-show="formData.length==0" size="small" @click="newTab">需要新增？</el-button>
          <el-button
            class="noMargin"
            type="text"
            style="color: #f56c6c;"
            size="small"
            @click="subSystemDelete()"
          >删除栏目</el-button>
        </div>
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

const api = {
  subSystem: "/script/subSystem",
  subSystemAdd: "/script/subSystemAdd",
  subSystemDelete: "/script/subSystemDelete",
};
export default {
  name: "ScriptColumn",
  props: {
    user_id: Number,
    formData: {
      default: [],
    },
  },
  data() {
    return {
      activeSystem: "",
      subSystem: [],
      subSystemName: "",
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
      this.$emit("subSystemClicked", this.subSystem[s].id);
    },
  },
  methods: {
    newTab() {
      this.$emit("newTab");
    },
    scriptLabelClicked(scriptName) {
      this.$emit("scriptNameClicked", scriptName);
    },
    //获取栏目
    async subSystemGet() {
      try {
        const { data: res } = await axios.get(api.subSystem, {
          user_id: this.user_id,
        });
        this.subSystem = [];
        for (let x = 0; x < res.data.length; x++) {
          this.subSystem.push({
            id: res.data[x]["id"],
            title: res.data[x]["name"],
          });
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    //添加栏目
    async subSystemAdd() {
      try {
        const { data: res } = await axios.post(api.subSystemAdd, {
          sub_system_name: this.subSystemName,
          user_id: this.user_id,
        });
        this.subSystem = [];
        this.subSystemName = "";
        this.subSystemGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
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
            user_id: this.user_id,
          });
          this.$message({
            message: "成功！",
            type: "success",
          });
          this.subSystemGet();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error",
          });
        }
      });
    },
  },
  mounted() {
    this.subSystemGet();
  },
};
</script>

<style scoped>
.noMargin {
  margin: 0;
}
</style>
