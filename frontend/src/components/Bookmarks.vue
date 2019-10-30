<template>
  <div class="bookmarks-main">
    <div>{{user}}</div>
    <div>{{bookmarks}}</div>
    <el-row v-for="bookmarksSuite in bookmarksData" :key="bookmarksSuite">
      <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
        <el-button
          size="small"
          :icon="bookmark.icon"
          @click="buttonClicked(bookmark.url)"
          v-show="bookmark.type!=-1"
        >{{bookmark.name}}</el-button>
        <el-button
          size="small"
          :icon="bookmark.icon"
          @click="bookmarkAdd()"
          v-show="bookmark.type==-1"
        >{{bookmark.name}}</el-button>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
//import { bookmarksData } from "../api/bookmarks";

export default {
  name: "bookmarks",
  props: {
    user: String,
    bookmarksData: Array
  },
  watch: {
    bookmarksData(newVal, oldVal) {
      this.bookmarksData = newVal;
    }
  },
  data() {
    return {
      bookmarksData: []
    };
  },
  methods: {
    buttonClicked(bookmarkUrl) {
      console.log(bookmarkUrl);
      window.open(bookmarkUrl);
    },
    bookmarkAdd() {
      console.log("要增加？");
    }
  },
  mounted() {
    console.log(this.bookmarks);
    this.bookmarks[-1].push({
      icon: "el-icon-plus",
      id: -1,
      name: "增加",
      update_time: "",
      url: "",
      type: -1
    });
  }
};
</script>
<style scoped>
.bookmarksCard {
  padding: 0px;
}
.el-button--small > span {
  margin-left: 5px;
}
</style>
