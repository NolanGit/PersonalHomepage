<template>
  <section>
    <el-row class="main-row margin_bottom-medium" :gutter="20">
      <el-col :span="5" class="lift-side-bar">
        <ConsoleScriptColumn
          :user_id="user_id"
          :formData="formData"
          @subSystemClicked="subSystemClicked"
          @scriptNameClicked="scriptNameClicked"
        />
      </el-col>
      <el-col :span="19" class="right-side-bar">
        <ConsoleScriptDetail :systemId="systemId" :user_id="user_id" @formData="formDataChanged"/>
      </el-col>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
import { deepClone } from "../../js/common";
import ConsoleScriptColumn from "./ConsoleScriptColumn";
import ConsoleScriptDetail from "./ConsoleScriptDetail";

const api = {
  subSystem: "/script/subSystem",
  subSystemAdd: "/script/subSystemAdd",
  subSystemDelete: "/script/subSystemDelete"
};
export default {
  name: "ConsoleScript",
  components: {
    ConsoleScriptColumn,
    ConsoleScriptDetail
  },
  props: {
    user_id: Number
  },
  data() {
    return {
      systemId: Number,
      formData: []
    };
  },
  watch: {},
  methods: {
    subSystemClicked(systemId) {
      this.systemId = systemId;
    },
    formDataChanged(formData){
      this.formData=formData
    }
  }
};
</script>

<style>
</style>
