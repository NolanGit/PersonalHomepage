// widget的按钮区域
<template>
  <el-row type="flex" justify="center">
    <el-tooltip class="item" effect="dark" content="新增" placement="top">
      <el-button
        class="margin_left-mini margin_right-mini"
        size="small"
        @click="add()"
        icon="el-icon-plus"
        circle
        v-if="buttons.indexOf('add')!= -1"
      ></el-button>
    </el-tooltip>
    <el-tooltip class="item" effect="dark" content="编辑和排序" placement="top">
      <el-button
        class="bmargin_left-mini margin_right-mini"
        size="small"
        @click="sort()"
        icon="el-icon-setting"
        circle
        v-if="buttons.indexOf('sort')!= -1"
      ></el-button>
    </el-tooltip>
    <el-tooltip class="item" effect="dark" content="设置" placement="top">
      <el-button
        class="bmargin_left-mini margin_right-mini"
        size="small"
        @click="setting()"
        icon="el-icon-setting"
        circle
        v-if="buttons.indexOf('setting')!= -1"
      ></el-button>
    </el-tooltip>
    <el-tooltip class="item" effect="dark" content="推送" placement="top">
      <el-button
        class="margin_left-mini margin_right-mini"
        size="small"
        @click="notify()"
        icon="el-icon-bell"
        circle
        v-if="buttons.indexOf('notify')!= -1"
      ></el-button>
    </el-tooltip>
    <el-tooltip class="item" effect="dark" content="时间机器" placement="top">
      <el-button
        class="margin_left-mini margin_right-mini"
        size="small"
        @click="revert()"
        icon="el-icon-refresh-left"
        circle
        v-if="buttons.indexOf('revert')!= -1"
      ></el-button>
    </el-tooltip>
  </el-row>
</template>
<script>
export default {
  name: "WidgetButton",
  props: {
    buttons: Array,
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
    },
    revert() {
      this.$emit("revert");
    },
  },
};
</script>
<style scoped>
</style>
