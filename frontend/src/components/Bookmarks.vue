<template>
  <div class="bookmarks-main">
    <div>{{user}}</div>
    <div>{{bookmarks}}</div>
    <el-row v-for="bookmarksSuite in bookmarksData" :key="bookmarksSuite">
      <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
        <el-card shadow="hover">
          <td>
            <i :class="bookmark.icon"></i>
          </td>
          <td>
            <el-button type="text" @click="buttonClicked(bookmark.url)">{{bookmark.name}}</el-button>
          </td>
        </el-card>
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
      console.log("value changed 1", newVal);
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
      window.open(bookmarkUrl);
    }
  },
  mounted() {
    console.log(this.bookmarks);
  }
};
</script>
<style scoped>
</style>
