<template>
  <div class="bookmarks-main">
    <div>{{user}}</div>
    <div>{{bookmarks}}</div>
    <el-row v-for="bookmarksSuite in bookmarksData" :key="bookmarksSuite">
      <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
        <el-button size="small" :icon="bookmark.icon" @click="buttonClicked(bookmark.url)">{{bookmark.name}}</el-button>
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
    }
  },
  mounted() {
    console.log(this.bookmarks);
  }
};
</script>
<style scoped>
.bookmarksCard {
  padding: 0px;
}
.el-button [class*=el-icon-]+span {
    margin-left: 5px;
}
</style>
