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

    <el-row type="flex" justify="center" class="bookmarkButtons" v-if="user!=''">
      <el-popover placement="top" width="260" v-model="bookmarksPopover.visible">
        <p>添加书签：</p>
        <el-input size="mini" v-model="bookmarksPopover.name" placeholder="网站名称"></el-input>
        <el-input size="mini" v-model="bookmarksPopover.url" placeholder="链接(需要完整填写，包括'http://')"></el-input>
        <el-input size="mini" v-model="bookmarksPopover.icon" placeholder="图标名称"></el-input>
        <div style="text-align: right; margin: 0">
          <el-button type="primary" size="mini" @click="bookmarksAddButton()">确定</el-button>
        </div>
        <el-button size="small" slot="reference" icon="el-icon-plus" circle></el-button>
      </el-popover>
      <el-button size="small" @click="bookmarksSetting()" icon="el-icon-setting" circle></el-button>
    </el-row>

    <!--编辑界面-->
    <el-dialog
      title="编辑书签"
      :visible.sync="bookmarksEdit.visible"
      :close-on-click-modal="false"
      width="40%"
    >
      <SlickList lockAxis="y" v-model="bookmarksDataArray">
        <SlickItem
          v-for="(item, index) in bookmarksDataArray"
          :index="index"
          :key="index"
        >{{ item }}</SlickItem>
      </SlickList>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import { bookmarksAdd } from "../api/bookmarks";
import { SlickList, SlickItem } from "vue-slicksort";

export default {
  name: "bookmarks",
  props: {
    user: String,
    bookmarksData: Array
  },
  components: {
    SlickItem,
    SlickList
  },
  watch: {
    bookmarksData(newVal, oldVal) {
      this.bookmarksDataAddAddButton(newVal);
    }
  },
  data() {
    return {
      bookmarksDataArray: [],
      bookmarksEdit: {
        visible: false,
        list:[]
      },
      bookmarksPopover: {
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
    bookmarksAddButton() {
      var para = {
        url: this.bookmarksPopover.url,
        name: this.bookmarksPopover.name,
        icon: this.bookmarksPopover.icon,
        user: sessionStorage.getItem("user").replace(/\"/g, "")
      };
      bookmarksAdd(para).then(data => {
        if (data["code"] !== 200) {
          this.$message({
            message: data["msg"],
            type: "error"
          });
        } else {
          this.$message({
            message: data["msg"],
            type: "success"
          });
        }
      });
      this.bookmarksPopover.url = "https://";
      this.bookmarksPopover.name = "";
      this.bookmarksPopover.icon = "";
    },
    bookmarksDataAddAddButton(bookmarksData) {
      this.bookmarksDataArray = bookmarksData;
      for(var x=0;x<this.bookmarksDataArray.length;x++){
        this.bookmarksEdit.list.push(
          this.bookmarksDataArray[x].name
        )
      }
    },
    bookmarksSetting() {
      this.bookmarksEdit.visible = true;
    }
  },
  mounted() {}
};
</script>
<style scoped>
.bookmarks-main {
  min-height: 280px;
}
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
.bookmarkButtons {
  margin-top: 20px;
}
</style>
