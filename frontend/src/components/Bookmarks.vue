<template>
  <div class="bookmarks-main">
    <div>{{user}}</div>
    <div>{{bookmarks}}</div>
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
        <el-button
          class="bookmarkButton"
          size="small"
          @click="bookmarkAdd()"
          v-show="bookmark.type==-1"
        >
          <i :class="bookmark.icon" style="margin-right=5px;font-size=15px"></i>
          {{bookmark.name}}
        </el-button>
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
      bookmarksDataTemp: []
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
        if (bookmarksData.length != 0) {
          console.log("bookmarksData1");
          console.log(bookmarksData);
          if (bookmarksData[bookmarksData.length - 1].length == 4) {
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
        } else {
        }
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
</style>
