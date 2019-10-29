<template>
  <div class="bookmarks-main">
    <el-row :gutter="20" v-for="bookmarksSuite in bookmarks" :key="bookmarksSuite">
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
  data() {
    return {
      bookmarks: []
    };
  },
  methods: {
    buttonClicked(bookmark) {
      console.log(bookmark);
    }
  },
  mounted() {
    var para = {
      user: "孙浩然"
    };
    bookmarksData(para).then(data => {
      if (data["code"] !== 200) {
        this.$message({
          message: data["msg"],
          type: "error"
        });
      } else {
        console.log(data);
      }
    });
  }
};
</script>
<style scoped>
</style>
