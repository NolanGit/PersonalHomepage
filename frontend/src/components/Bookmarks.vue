<template>
  <div class="bookmarks-main">
    <el-row type="flex" justify="center">
      <div>
        <div class="bookmarks">书签</div>
      </div>
    </el-row>
    <el-row v-for="bookmarksSuite in bookmarksData" :key="bookmarksSuite">
      <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
        <el-button
          class="bookmarkButton"
          size="small"
          @click="buttonClicked(bookmark.url)"
          v-show="bookmark.type!=-1"
        >
          <i :class="bookmark.icon" style="margin-right=5px;font-size=15px"></i>
          {{bookmark.name}}
        </el-button>
        <el-popover placement="top" width="260" v-model="bookmarkPopover.visible">
          <p>添加城市：</p>
          <el-input size="mini" v-model="bookmarkPopover.name" placeholder="网站名称"></el-input>
          <el-input size="mini" v-model="bookmarkPopover.url" placeholder="链接(需要完整填写，包括'http://')"></el-input>
          <el-input size="mini" v-model="bookmarkPopover.icon" placeholder="图标名称"></el-input>
          <div style="text-align: right; margin: 0">
            <el-button type="primary" size="mini" @click="addLocation()">确定</el-button>
          </div>
          <el-button
            class="bookmarkButton"
            size="small"
            @click="bookmarkAdd()"
            v-show="bookmark.type==-1"
          >
            <i :class="bookmark.icon" style="margin-right=5px;font-size=15px"></i>
            {{bookmark.name}}
          </el-button>
        </el-popover>
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
      this.bookmarksDataAddAddButton(newVal);
    }
  },
  data() {
    return {
      bookmarksData: [],
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
      console.log("要增加？");
    },
    bookmarksDataAddAddButton(bookmarksData) {
      if (this.bookmarksDataTemp == bookmarksData) {
        return;
      } else {
        console.log("bookmarksData1");
        console.log(bookmarksData);
        if (
          (bookmarksData[bookmarksData.length - 1].length == 4) |
          (bookmarksData[bookmarksData.length - 1].length == 0)
        ) {
          bookmarksData.push([
            {
              icon: "el-icon-plus",
              id: -1,
              name: "增加",
              update_time: "",
              url: "",
              type: -1
            }
          ]);
        } else {
          bookmarksData[bookmarksData.length - 1].push({
            icon: "el-icon-plus",
            id: -1,
            name: "增加",
            update_time: "",
            url: "",
            type: -1
          });
        }
        this.bookmarksData = bookmarksData;
        this.bookmarksDataTemp = bookmarksData;
        console.log("bookmarksData2");
        console.log(bookmarksData);
      }
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
}
</style>
