<template>
  <section>
    <el-button
      :loading="submitButtonLoading"
      type="primary"
      style="margin:20px 20px 20px 20px;position:absolute;bottom:0;right:0;z-index:99"
      @click="submit()"
      v-show="formData.length!=0"
    >提交</el-button>

    <!--运行界面-->
    <el-drawer
      title="输出"
      :v-if="output.visible"
      :visible.sync="output.visible"
      size="70%"
      direction="btt"
      :before-close="outputDialogClose"
    >
      <div class="margin_left-medium margin_right-medium">
        <el-card shadow="hover">
          <div class="output-div" ref="outputDialog">
            <div class="output-html" v-html="output.text"></div>
          </div>
        </el-card>
      </div>
      <div class="dialog-footer" v-show="output.canBeTerminate">
        <el-button size="small" plain type="danger" @click.native="terminate()">停止运行</el-button>
      </div>
    </el-drawer>
  </section>
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
  name: "ConsoleScriptRun",
  props: {
    user_id: Number,
    formData: {
      default: []
    }
  },
  watch: {},
  data() {
    return {
      output: {
        canBeTerminate: false,
        loading: false,
        log_id: 0,
        logs: [],
        visible: false,
        text: "",
        important_fields: [],
        isAlert: false
      }
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
    }
  },
  methods: {
    scriptLabelClicked(scriptName) {
      this.$emit("scriptNameClicked", scriptName);
    },
    //获取栏目
    async subSystemGet() {
      try {
        const { data: res } = await axios.get(api.subSystem, {
          user_id: this.user_id
        });
        for (let x = 0; x < res.data.length; x++) {
          this.subSystem.push({
            id: res.data[x]["id"],
            title: res.data[x]["name"]
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
    //添加栏目
    async subSystemAdd() {
      try {
        const { data: res } = await axios.post(api.subSystemAdd, {
          sub_system_name: this.subSystemName,
          user_id: this.user_id
        });
        this.subSystem = [];
        this.subSystemGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
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
            user_id: this.user_id
          });
          this.$message({
            message: "成功！",
            type: "success"
          });
          this.subSystemGet();
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
    this.subSystemGet();
  }
};
</script>

<style>
</style>
