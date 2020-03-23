// 拖动排序组件，接受一个Array，每一组数据必须有name参数，点击提交后返回带顺序的Array，点击编辑则返回目标组的数据和index
<template>
  <el-row type="flex" justify="center" class="margin_top-medium" v-show="user_id!=0">
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
    user_id: Number,
    widget_id: Number,
    buttons: Array
  },
  watch: {
    user_id(newValue, oldValue) {}
  },
  data() {
    return {};
  },
  methods: {
    edit(item, index) {
      this.$emit("edit", item, index);
    },
    del(item, index) {
      this.list.splice(index, 1);
    },
    submit() {
      this.$emit("submit", this.list);
    }
  }
};
</script>
<style scoped>
</style>
