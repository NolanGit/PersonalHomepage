<template>
  <div class="bookmarks-main">
    <el-row type="flex" justify="center">
      <div>
        <div class="bookmarks-label">书签</div>
      </div>
    </el-row>

    <div class="bookmarks-data-row">
      <el-row v-for="bookmarksSuite in bookmarksDataArray" :key="bookmarksSuite">
        <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
          <el-button
            class="bookmarks-main-button"
            size="small"
            @click="bookmarksClicked(bookmark.url)"
          >
            <i :class="bookmark.icon" style="margin-right=5px;font-size=15px"></i>
            {{bookmark.name}}
          </el-button>
        </el-col>
      </el-row>
    </div>

    <el-row type="flex" justify="center" class="bookmarks-option-button" v-show="user!=undefined">
      <el-button
        class="bookmarks-option-button-add"
        size="small"
        @click="bookmarksOptionButtonAddClicked()"
        icon="el-icon-plus"
        circle
      ></el-button>
      <el-button
        class="bookmarks-option-button-edit-form"
        size="small"
        @click="bookmarksOptionButtonSettingDialogClicked()"
        icon="el-icon-setting"
        circle
      ></el-button>
    </el-row>

    <!--编辑界面-->
    <el-dialog title="新增书签" :visible.sync="bookmarksEditForm.visible" width="40%">
      <el-form ref="form" :model="bookmarksEditForm" label-width="80px">
        <el-form-item label="网站名称">
          <el-input
            class="edit-form-name"
            size="small"
            v-model="bookmarksEditForm.name"
            placeholder="网站名称"
          ></el-input>
        </el-form-item>
        <el-form-item label="链接">
          <el-input
            class="edit-form-url"
            size="small"
            v-model="bookmarksEditForm.url"
            placeholder="链接(需要完整填写，包括'http://')"
          ></el-input>
        </el-form-item>
        <el-form-item label="图标名称">
          <el-input
            class="edit-form-icon"
            size="small"
            v-model="bookmarksEditForm.icon"
            placeholder="图标名称"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            class="edit-form-confirm"
            type="primary"
            size="small"
            @click="bookmarksAddFront()"
          >确定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!--编辑界面-->
    <el-dialog title="编辑书签" :visible.sync="bookmarksEdit.visible" width="40%">
      <SlickList lockAxis="y" v-model="bookmarksEdit.list" class="slick_list">
        <SlickItem
          class="slick_list_item"
          v-for="(item, index) in bookmarksEdit.list"
          :index="index"
          :key="index"
        >
          <i class="el-icon-s-operation"></i>
          <span>{{ item }}</span>
          <i class="el-icon-setting" @click="bookmarksSetting(item)"></i>
          <i class="el-icon-delete" @click="bookmarksDelete(item)"></i>
        </SlickItem>
      </SlickList>
      <el-button
        class="edit-form-confirm"
        type="primary"
        size="small"
        @click="bookmarksEditSubmit()"
      >确定</el-button>
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
    // bookmarksEditData(newVal, oldVal) {
    //   this.bookmarksEditDataInit(newVal);
    // }
  },
  data() {
    return {
      bookmarksDataArray: [],
      bookmarksEdit: {
        visible: false,
        list: []
      },
      bookmarksEditForm: {
        visible: false,
        name: "",
        url: "https://",
        icon: ""
      }
    };
  },
  methods: {
    bookmarksClicked(bookmarkUrl) {
      console.log(bookmarkUrl);
      window.open(bookmarkUrl);
    },
    bookmarksAddFront() {
      var para = {
        url: this.bookmarksEditForm.url,
        name: this.bookmarksEditForm.name,
        icon: this.bookmarksEditForm.icon,
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
      this.bookmarksEditForm.url = "https://";
      this.bookmarksEditForm.name = "";
      this.bookmarksEditForm.icon = "";
    },
    bookmarksDataInit(bookmarksData) {
      this.bookmarksDataArray = bookmarksData;
    },
    bookmarksEditDataInit(bookmarksEditData) {
      this.bookmarksEdit.list = bookmarksEditData;
    },
    bookmarksOptionButtonAddClicked() {
      this.bookmarksEditForm.visible = true;
    },
    bookmarksOptionButtonSettingDialogClicked() {
      var temp = [];
      for (let x = 0; x < this.bookmarksDataArray.length; x++) {
        for (let y = 0; y < this.bookmarksDataArray[x].length; y++) {
          temp.push(this.bookmarksDataArray[x][y].name);
        }
      }
      console.log(temp);
      this.bookmarksEdit.list = temp;
      this.bookmarksEdit.visible = true;
    },
    bookmarksEditSubmit(){
      console.log(bookmarksEdit.list)
    },
    bookmarksSetting(item){
      console.log(item)
    },
    bookmarksDelete(item){
      console.log(item)
    },
  },
  created() {},
  mounted() {}
};
</script>
<style scoped>
.bookmarks-main {
  min-height: 280px;
}
.bookmarks-label {
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
  font-weight: 600;
  font-size: 20px;
  color: #303133;
  padding-bottom: 20px;
}
.bookmarks-data-row {
  min-height: 210px;
}
.bookmarks-main-button {
  width: 90px;
  height: 40px;
}
.bookmarks-option-button {
  margin-top: 20px;
}
.bookmarks-option-button-add {
  margin-left: 5px;
  margin-right: 5px;
}
.bookmarks-option-button-edit-form {
  margin-left: 5px;
  margin-right: 5px;
}
.slick_list {
  max-height: 80vh;
  margin: 0 auto;
  padding: 0;
  overflow: auto;
  border: 1px solid #efefef;
  max-width: 600px;
  cursor: pointer;
}
.slick_list_item {
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
.edit-form-name {
  width: 70%;
}
.edit-form-url {
  width: 70%;
}
.edit-form-icon {
  width: 70%;
}
</style>
