<template>
  <div class="bookmarks-main">
    <el-row type="flex" justify="center">
      <div>
        <div class="bookmarks">书签</div>
      </div>
    </el-row>
    <el-row v-for="bookmarksSuite in bookmarksDataArray" :key="bookmarksSuite">
      <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
        <el-button class="bookmarkButton" size="small" @click="buttonClicked(bookmark.url)">
          <i :class="bookmark.icon" style="margin-right=5px;font-size=15px"></i>
          {{bookmark.name}}
        </el-button>
      </el-col>
    </el-row>

    <el-popover placement="top" width="160" v-model="bookmarkPopover.visible">
      <p>添加书签：</p>
      <el-input size="mini" v-model="bookmarkPopover.name" placeholder="网站名称"></el-input>
      <el-input size="mini" v-model="bookmarkPopover.url" placeholder="链接(需要完整填写，包括'http://')"></el-input>
      <el-input size="mini" v-model="bookmarkPopover.icon" placeholder="图标名称"></el-input>
      <div style="text-align: right; margin: 0">
        <el-button type="primary" size="mini" @click="bookmarkAdd()">确定</el-button>
      </div>
      <el-button class="bookmarkButton" size="small" slot="reference" icon="el-icon-plus"></el-button>
    </el-popover>
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
      this.bookmarksDataAddAddButton(newVal);
    }
  },
  data() {
    return {
      bookmarksDataArray: [],
      bookmarksDataTemp: [],
      bookmarkPopover: {
        visible: false,
        name: "",
        url: "https://",
        icon: ""
      }
    };
  },
  methods: {
    buttonClicked(bookmarkUrl) {
      console.log(bookmarkUrl);
      window.open(bookmarkUrl);
    },
    bookmarkAdd() {
      this.bookmarkPopover.url = "https://";
      this.bookmarkPopover.name = "";
      this.bookmarkPopover.icon = "";
    },
    bookmarksDataAddAddButton(bookmarksData) {
      this.bookmarksDataArray = bookmarksData;
    }
  },
  mounted() {}
};
</script>
<style scoped>
.bookmarksCard {
  padding: 0px;
}
.bookmarkButton {
  width: 90px;
  height: 40px;
}
.bookmarks {
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
  font-weight: 600;
  font-size: 20px;
  color: #303133;
  padding-bottom: 20px;
}
</style>
