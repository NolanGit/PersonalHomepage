<template>
  <div class="bookmarks-main">
    <div>{{user}}</div>
    <div>{{bookmarks}}</div>
    <el-row v-for="bookmarksSuite in bookmarks" :key="bookmarksSuite">
      <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
        <el-card>
          <el-button type="text" @click="buttonClicked(bookmark)">{{bookmark.name}}</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import { bookmarksData } from "../api/bookmarks";

export default {
  name: "bookmarks",
  props: {
    user: String,
    bookmarks:Array,
  },
  data() {
    return {
    };
  },
  methods: {
    buttonClicked(bookmark) {
      console.log(bookmark);
    }
  },
  mounted() {
    console.log(bookmarks)
  }
};
</script>
<style scoped>
</style>
