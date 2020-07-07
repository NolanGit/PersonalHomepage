// widget的按钮区域
<template>
  <el-row type="flex" justify="center" class="margin_top-medium">
    <el-button
      class="margin_left-mini margin_right-mini"
      size="small"
      @click="add()"
      icon="el-icon-plus"
      circle
      v-if="buttons.indexOf('add')!= -1"
    ></el-button>
    <el-button
      class="bmargin_left-mini margin_right-mini"
      size="small"
      @click="sort()"
      icon="el-icon-setting"
      circle
      v-if="buttons.indexOf('sort')!= -1"
    ></el-button>
    <el-button
      class="bmargin_left-mini margin_right-mini"
      size="small"
      @click="setting()"
      icon="el-icon-setting"
      circle
      v-if="buttons.indexOf('setting')!= -1"
    ></el-button>
    <el-button
      class="margin_left-mini margin_right-mini"
      size="small"
      @click="notify()"
      icon="el-icon-bell"
      circle
      v-if="buttons.indexOf('notify')!= -1"
    ></el-button>
  </el-row>
</template>
<script>
export default {
  name: "WidgetButton",
  props: {
    buttons: Array
  },
  data() {
    return {};
  },
  methods: {
    add() {
      this.$emit("add");
    },
    sort() {
      this.$emit("sort");
    },
    setting() {
      this.$emit("setting");
    },
    notify() {
      this.$emit("notify");
    }
  }
};
</script>
<style scoped>
</style>
