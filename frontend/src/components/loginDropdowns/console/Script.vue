<template>
  <section>
    <el-row class="main-row margin_bottom-medium" :gutter="20">
      <el-col :span="5" class="lift-side-bar">
        <ScriptColumn
          :user_id="user_id"
          :formData="formData"
          @newTab="newTab"
          @subSystemClicked="subSystemClicked"
          @scriptNameClicked="scriptNameClicked"
        />
      </el-col>
      <el-col :span="19" class="right-side-bar">
        <ScriptDetail
          :activeScriptName="scriptName"
          :systemId="systemId"
          :user_id="user_id"
          :newTabBool="newTabBool"
          @formData="formDataChanged"
        />
      </el-col>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
import ScriptColumn from "./ScriptColumn";
import ScriptDetail from "./ScriptDetail";

const api = {
  subSystem: "/script/subSystem",
  subSystemAdd: "/script/subSystemAdd",
  subSystemDelete: "/script/subSystemDelete"
};
export default {
  name: "Script",
  components: {
    ScriptColumn,
    ScriptDetail
  },
  props: {
    user_id: Number
  },
  data() {
    return {
      systemId: Number,
      scriptName: String,
      newTabBool: false,
      formData: []
    };
  },
  watch: {},
  methods: {
    newTab() {
      this.newTabBool = true;
    },
    subSystemClicked(systemId) {
      this.systemId = systemId;
    },
    scriptNameClicked(scriptName) {
      this.scriptName = scriptName;
    },
    formDataChanged(formData) {
      this.formData = formData;
    }
  }
};
</script>

<style>
</style>
