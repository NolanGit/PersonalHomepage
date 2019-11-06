<template>
  <div class="bookmarks-main">
    <el-row type="flex" justify="center">
      <div>
        <div class="bookmarks">书签</div>
      </div>
    </el-row>
    <el-row
      class="bookmarksData"
      v-for="bookmarksSuite in bookmarksDataArray"
      :key="bookmarksSuite"
    >
      <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
        <el-button class="bookmarksButton" size="small" @click="buttonClicked(bookmark.url)">
          <i :class="bookmark.icon" style="margin-right=5px;font-size=15px"></i>
          {{bookmark.name}}
        </el-button>
      </el-col>
    </el-row>

    <el-row type="flex" justify="center" class="bookmarksOptionButton" v-show="user!=''">
      <el-popover placement="top" width="260" v-model="bookmarksPopover.visible">
        <p>添加书签：</p>
        <el-input size="mini" v-model="bookmarksPopover.name" placeholder="网站名称"></el-input>
        <el-input size="mini" v-model="bookmarksPopover.url" placeholder="链接(需要完整填写，包括'http://')"></el-input>
        <el-input size="mini" v-model="bookmarksPopover.icon" placeholder="图标名称"></el-input>
        <div style="text-align: right; margin: 0">
          <el-button type="primary" size="mini" @click="bookmarksAddButton()">确定</el-button>
        </div>
        <el-button
          class="bookmarksOptionButtonAdd"
          size="small"
          slot="reference"
          icon="el-icon-plus"
          circle
        ></el-button>
      </el-popover>

      <el-button
        class="bookmarksOptionButtonSetting"
        size="small"
        @click="bookmarksSetting()"
        icon="el-icon-setting"
        circle
      ></el-button>
    </el-row>

    <!--编辑界面-->
    <el-dialog title="编辑书签" :visible.sync="bookmarksEdit.visible" width="40%">
      <SlickList axis="x" lockAxis="x" v-model="bookmarksEdit.list" class="list">
        <SlickItem
          class="list-item"
          v-for="(item, index) in bookmarksEdit.list"
          :index="index"
          :key="index"
        ><SlickList :lockToContainerEdges="true" class="list" lockAxis="y" v-model="item.itemArr">
                    <SlickItem class="list-item" v-for="(singleItem, singleIndex) in item" :index="singleIndex" :key="singleIndex">
                        {{ singleItem }}
                    </SlickItem>
                </SlickList>
          <!-- <span>{{ item }}</span>
          <el-button
            class="list-button"
            size="small"
            @click="bookmarksDelete()"
            icon="el-icon-delete"
            circle
          ></el-button> -->
        </SlickItem>
      </SlickList>
    </el-dialog>

  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import { bookmarksAdd } from "../api/bookmarks";
import { SlickList, SlickItem } from "vue-slicksort";
import { ContainerMixin, ElementMixin } from "vue-slicksort";

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
      this.bookmarksDataInit(newVal);
    }
  },
  data() {
    return {
      msg: "Hello, This is Vue-Slicksort-Demo ！",
      flag: true,
      list: [
        {
          title: "list1"
        },
        {
          title: "list2"
        },
        {
          title: "list3"
        },
        {
          title: "list4"
        },
        {
          title: "list5"
        }
      ],
      items: [
        {
          name: "title1",
          itemArr: ["Item1", "Item2", "Item3"]
        },
        {
          name: "title2",
          itemArr: ["Item4", "Item5", "Item6"]
        },
        {
          name: "title3",
          itemArr: ["Item7", "Item8", "Item9"]
        }
      ],
      bookmarksDataArray: [],
      bookmarksEdit: {
        visible: false,
        list: []
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
    bookmarksDataInit(bookmarksData) {
      this.bookmarksDataArray = bookmarksData;
      console.log(this.bookmarksDataArray);
      this.bookmarksEdit.list=this.bookmarksDataArray
      // for (var x = 0; x < this.bookmarksDataArray.length; x++) {
      //   for (var y = 0; y < this.bookmarksDataArray[x].length; y++) {
      //     this.bookmarksEdit.list.push(this.bookmarksDataArray[x][y].name);
      //   }
      // }
      console.log(this.bookmarksEdit.list);
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
.bookmarksButton {
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
.bookmarksOptionButton {
  margin-top: 20px;
}
.bookmarksData {
  min-height: 210px;
}
.bookmarksOptionButtonAdd {
  margin-left: 5px;
  margin-right: 5px;
}
.bookmarksOptionButtonSetting {
  margin-left: 5px;
  margin-right: 5px;
}
.list {
  max-height: 80vh;
  margin: 0 auto;
  padding: 0;
  overflow: auto;
  background-color: #f3f3f3;
  border: 1px solid #efefef;
  max-width: 600px;
  cursor: pointer;
}
.list-item {
  list-style: none;
  padding: 10px 0;
  height: 40px;
  width: 100%;
  color: #606266;
  font-size: 14px;
  z-index: 3000;
  box-sizing: border-box;
  user-select: none;
  display: flex;
  align-items: center;
  width: 100%;
  padding: 20px;
  background-color: #fff;
  border-bottom: 1px solid #efefef;
  box-sizing: border-box;
  user-select: none;
  color: #333;
  font-weight: 400;
}
</style>
