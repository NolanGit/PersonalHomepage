<template>
  <section>
    <el-row class="main-row margin_bottom-medium" :gutter="20">
      <el-col :span="5" class="lift-side-bar">
        <ConsoleScriptColumn />
      </el-col>
      <el-col :span="19" class="right-side-bar"></el-col>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
import { deepClone } from "../../js/common";
import ConsoleScriptColumn from "./ConsoleScriptColumn";
const api = {
  subSystem: "/script/subSystem",
  subSystemAdd: "/script/subSystemAdd",
  subSystemDelete: "/script/subSystemDelete"
};
export default {
  name: "ConsoleScript",
  components: {
    ConsoleScriptColumn
  },
  props: {
    user_id: Number
  },
  data() {
    return {};
  },
  watch: {},
  methods: {}
};
</script>

<style>
</style>