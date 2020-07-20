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
  run: "/script/run",
  terminate: "/script/terminate",
  runOutput: "/script/runOutput",
  edit: "/script/edit",
  delete: "/script/delete",
  saveOutput: "/script/saveOutput",
  extraButtonScriptRun: "/script/extraButtonScriptRun",
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
  watch: {},
  methods: {},
  mounted() {}
};
</script>

<style>
</style>
