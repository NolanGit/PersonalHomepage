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
    <div>
      <h3 class="message">{{ msg }}</h3>
      <hr />
      <h4>Demo1 : list in Y-axis</h4>
      <SlickList :lockToContainerEdges="true" class="list" lockAxis="y" v-model="list">
        <SlickItem
          class="list-item"
          v-for="(item, index) in list"
          :index="index"
          :key="index"
        >{{ item.title }}</SlickItem>
      </SlickList>
      <hr />
      <h4>Demo2 : parent item in X-axis , children item in Y-ais</h4>
      <SlickList
        :lockToContainerEdges="true"
        axis="x"
        lockAxis="x"
        v-model="items"
        class="SortableList"
        @input="getChangeLists"
      >
        <SlickItem v-for="(item, index) in items" class="SortableItem" :index="index" :key="index">
          {{ item.name }}
          <SlickList :lockToContainerEdges="true" class="list" lockAxis="y" v-model="item.itemArr">
            <SlickItem
              class="list-item"
              v-for="(item, index) in item.itemArr"
              :index="index"
              :key="index"
            >{{ item }}</SlickItem>
          </SlickList>
        </SlickItem>
      </SlickList>
      <hr />
      <h4>Demo3 : parent item in Y-axis , children item in Y-ais</h4>
      <SlickList
        :lockToContainerEdges="true"
        lockAxis="y"
        v-model="items"
        class="SortableList2"
        @input="getChangeLists"
      >
        <SlickItem v-for="(item, index) in items" class="SortableItem2" :index="index" :key="index">
          <p>{{ item.name }}</p>
          <SlickList :lockToContainerEdges="true" class="list" lockAxis="y" v-model="item.itemArr">
            <SlickItem
              class="list-item"
              v-for="(item, index) in item.itemArr"
              :index="index"
              :key="index"
            >{{ item }}</SlickItem>
          </SlickList>
        </SlickItem>
      </SlickList>
    </div>
    <!--编辑界面-->
    <el-dialog
      title="编辑书签"
      :visible.sync="bookmarksEdit.visible"
      :close-on-click-modal="false"
      width="40%"
    >
      <SlickList lockAxis="y" v-model="bookmarksEdit.list" class="list">
        <SlickItem
          class="list-item"
          v-for="(item, index) in bookmarksEdit.list"
          :index="index"
          :key="index"
        >
          <span>{{ item }}</span>
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
      for (var x = 0; x < this.bookmarksDataArray.length; x++) {
        for (var y = 0; y < this.bookmarksDataArray[x].length; y++) {
          this.bookmarksEdit.list.push(this.bookmarksDataArray[x][y].name);
        }
      }
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
.stylizedHelper {
  background: blue;
  color: #fff;
}
.SortableList {
  display: flex;
  width: 600px;
  white-space: nowrap;
  max-height: 80vh;
  margin: 0 auto;
  padding: 0;
  overflow: auto;
  background-color: #f3f3f3;
  border: 1px solid #efefef;
  cursor: pointer;
}
.SortableItem {
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
  border: 1px solid #ccc;
}
.SortableList2 {
  width: 300px;
  margin: 20px auto;
  border: 1px solid #efefef;
}
.SortableItem2 {
  width: 300px;
  border: 1px solid #efefef;
  text-align: center;
}
.SortableItem2 p {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  background: #efefef;
  margin: 0;
  height: 30px;
}
</style>
