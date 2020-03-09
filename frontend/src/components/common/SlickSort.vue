// 拖动排序组件，接受一个Array，每一组数据必须有name参数，点击提交后返回带顺序的Array，点击编辑则返回目标组的数据和index
<template>
  <div>
    <el-row>
      <SlickList lockAxis="y" v-model="list" class="slick_list">
        <SlickItem
          class="slick_list_item"
          v-for="(item, index) in list"
          :index="index"
          :key="index"
        >
          <i class="el-icon-s-operation" style="color: #6a6c70;"></i>
          <span class="slick_list_item_span">{{ item.name }}</span>
          <div class="slick_list_item_button">
            <el-button size="mini" class="el-icon-setting" @click="edit(item, index)"></el-button>
            <el-button type="danger" size="mini" class="el-icon-delete" @click="del(item, index)"></el-button>
          </div>
        </SlickItem>
      </SlickList>
    </el-row>
    <el-row class="margin_top-medium">
      <el-button class="edit-form-confirm" type="primary" size="small" @click="submit()">确定</el-button>
    </el-row>
  </div>
</template>
<script>
import { SlickList, SlickItem } from "vue-slicksort";

export default {
  name: "SlickSort",
  components: {
    SlickItem,
    SlickList
  },
  props: {
    list: Array
  },
  watch: {
    list(newValue, oldValue) {},
    deep: true
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
