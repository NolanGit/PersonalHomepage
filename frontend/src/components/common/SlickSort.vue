<template>
  <div>
    <SlickList lockAxis="y" v-model="list" class="slick_list">
      <SlickItem class="slick_list_item" v-for="(item, index) in list" :index="index" :key="index">
        <i class="el-icon-s-operation" style="color: #6a6c70;"></i>
        <span class="slick_list_item_span">{{ item.name }}</span>
        <div class="slick_list_item_button">
          <el-button size="mini" class="el-icon-setting" @click="set(item, index)"></el-button>
          <el-button type="danger" size="mini" class="el-icon-delete" @click="del(item, index)"></el-button>
        </div>
      </SlickItem>
    </SlickList>
    <span slot="footer" class="dialog-footer">
      <el-button class="edit-form-confirm" type="primary" size="small" @click="submit()">确定</el-button>
    </span>
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
    set(item, index) {
      this.$emit("set", item);
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
