<template>
  <div>
    <SlickList lockAxis="y" v-model="bookmarksEdit.list" class="slick_list">
      <SlickItem
        class="slick_list_item"
        v-for="(item, index) in bookmarksEdit.list"
        :index="index"
        :key="index"
      >
        <i class="el-icon-s-operation" style="color: #6a6c70;"></i>
        <span class="slick_list_item_span">{{ item.name }}</span>
        <div class="slick_list_item_button">
          <el-button size="mini" class="el-icon-setting" @click="bookmarksSetting(item, index)"></el-button>
          <el-button
            type="danger"
            size="mini"
            class="el-icon-delete"
            @click="bookmarksDeleteSubmit(item, index)"
          ></el-button>
        </div>
      </SlickItem>
    </SlickList>
    <span slot="footer" class="dialog-footer">
      <el-button
        class="edit-form-confirm"
        type="primary"
        size="small"
        @click="bookmarksEditSubmit()"
      >确定</el-button>
    </span>
  </div>
</template>
<script>
import axios from "axios";
import IconComponet from "./common/Icon.vue";
import { SlickList, SlickItem } from "vue-slicksort";
import { ContainerMixin, ElementMixin } from "vue-slicksort";
const api = {
  get: "/bookmarks/get",
  bookmarksAdd: "/bookmarks/bookmarksAdd",
  bookmarksEdit: "/bookmarks/bookmarksEdit",
  icon: "/icon"
};
export default {
  name: "bookmarks",
  props: {
    user_id: Number
  },
  components: {
    SlickItem,
    SlickList
  },
  data() {
    return {};
  },
  methods: {},
  mounted() {}
};
</script>
<style scoped>
</style>
