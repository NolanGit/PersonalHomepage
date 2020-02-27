<template>
  <div class="bookmarks-main">
    <el-row type="flex" justify="center">
      <div>
        <div class="widget-label">书签</div>
      </div>
    </el-row>

    <div class="bookmarks-data-row-main">
      <el-row
        class="margin_bottom-medium"
        v-for="bookmarksSuite in bookmarksDataArray"
        :key="bookmarksSuite"
      >
        <el-col :span="6" v-for="bookmark in bookmarksSuite" :key="bookmark">
          <el-button class="bookmarks-main-button" size="small" @click="bookmarksClicked(bookmark.url)">
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
        @click="bookmarksOptionButtonSettingClicked()"
        icon="el-icon-setting"
        circle
      ></el-button>
    </el-row>

    <!--编辑界面-->
    <el-dialog
      :title="bookmarksEditForm.title"
      :visible.sync="bookmarksEditForm.visible"
      width="40%"
    >
      <el-form ref="form" :model="bookmarksEditForm" size="mini">
        <el-form-item label="网站名称">
          <div class="div-flex">
            <el-input size="small" v-model="bookmarksEditForm.name" placeholder="网站名称"></el-input>
          </div>
        </el-form-item>
        <el-form-item label="网站链接">
          <div class="div-flex">
            <el-input
              size="small"
              v-model="bookmarksEditForm.url"
              placeholder="链接(需要完整填写，包括'http://')"
            ></el-input>
          </div>
        </el-form-item>
        <el-form-item label="图标名称">
          <div class="div-flex">
            <el-input size="small" v-model="bookmarksEditForm.icon" placeholder="图标名称" disabled></el-input>
            <el-button size="small" @click="bookmarksIconFront()">选择图标</el-button>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="bookmarksEditFormConfirmClicked()">确定</el-button>
      </span>
    </el-dialog>

    <!--编辑顺序界面-->
    <el-dialog title="编辑书签" :visible.sync="bookmarksEdit.visible" width="40%">
      <SlickList lockAxis="y" v-model="bookmarksEdit.list" class="slick_list">
        <SlickItem
          class="slick_list_item"
          v-for="(item, index) in bookmarksEdit.list"
          :index="index"
          :key="index"
        >
          <i class="el-icon-s-operation" style="color: #6a6c70;"></i>
          <span class="slick_list_item_span">{{ item.name }}</span>
          <div class="slick_list_item_button">
            <el-button size="mini" class="el-icon-setting" @click="bookmarksSetting(item, index)"></el-button>
            <el-button
              type="danger"
              size="mini"
              class="el-icon-delete"
              @click="bookmarksDeleteSubmit(item, index)"
            ></el-button>
          </div>
        </SlickItem>
      </SlickList>
      <span slot="footer" class="dialog-footer">
        <el-button
          class="edit-form-confirm"
          type="primary"
          size="small"
          @click="bookmarksEditSubmit()"
        >确定</el-button>
      </span>
    </el-dialog>

    <!--选择图标界面-->
    <el-dialog title="选择喜欢的图标" :visible.sync="icon.visible" width="70%">
      <IconComponet @iconName="iconNameGet" :icons="icon.data"></IconComponet>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import IconComponet from "./common/Icon.vue";
import { SlickList, SlickItem } from "vue-slicksort";
import { ContainerMixin, ElementMixin } from "vue-slicksort";
const api = {
  bookmarksAdd: "/bookmarks/bookmarksAdd",
  bookmarksEdit: "/bookmarks/bookmarksEdit",
  icon: "/icon"
};
export default {
  name: "bookmarks",
  props: {
    user: String,
    bookmarksData: Array
  },
  components: {
    SlickItem,
    SlickList,
    IconComponet
  },
  watch: {
    bookmarksData(newVal, oldVal) {
      this.bookmarksDataArray = newVal;
    }
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
      },
      bookmarksEditTempIndex: 0,
      icon: {
        visible: false,
        data: []
      }
    };
  },
  methods: {
    bookmarksClicked(bookmarkUrl) {
      window.open(bookmarkUrl);
    },
    async bookmarksEditFormConfirmClicked() {
      if (this.bookmarksEditForm.title == "新增书签") {
        try {
          const { data: res } = await axios.post(api.bookmarksAdd, {
            url: this.bookmarksEditForm.url,
            name: this.bookmarksEditForm.name,
            icon: this.bookmarksEditForm.icon,
            user: sessionStorage.getItem("user").replace(/\"/g, "")
          });
          this.$message({
            message: res["msg"],
            type: "success"
          });
          this.$emit("bookmarksUpdate");
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      } else if (this.bookmarksEditForm.title == "编辑书签") {
        const tempEditIndex = this.bookmarksEditTempIndex;
        this.bookmarksEdit.list[tempEditIndex].url = this.bookmarksEditForm.url;
        this.bookmarksEdit.list[
          tempEditIndex
        ].name = this.bookmarksEditForm.name;
        this.bookmarksEdit.list[
          tempEditIndex
        ].icon = this.bookmarksEditForm.icon;
      }
      this.bookmarksEditForm.visible = false;
    },
    bookmarksOptionButtonAddClicked() {
      this.bookmarksEditForm = {
        title: "新增书签",
        visible: true,
        name: "",
        url: "https://",
        icon: ""
      };
    },
    bookmarksOptionButtonSettingClicked() {
      var temp = [];
      for (let x = 0; x < this.bookmarksDataArray.length; x++) {
        for (let y = 0; y < this.bookmarksDataArray[x].length; y++) {
          temp.push({
            id: this.bookmarksDataArray[x][y].id,
            name: this.bookmarksDataArray[x][y].name,
            url: this.bookmarksDataArray[x][y].url,
            icon: this.bookmarksDataArray[x][y].icon
          });
        }
      }
      console.log(temp);
      this.bookmarksEdit.list = temp;
      this.bookmarksEdit.visible = true;
    },
    async bookmarksEditSubmit() {
      for (let x = 0; x < this.bookmarksEdit.list.length; x++) {
        this.bookmarksEdit.list[x].order = x + 1;
      }
      try {
        const { data: res } = await axios.post(api.bookmarksEdit, {
          bookmarks: this.bookmarksEdit.list,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
        });
        this.$message({
          message: res["msg"],
          type: "success"
        });
        this.bookmarksEdit.visible = false;
        this.$emit("bookmarksUpdate");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    bookmarksSetting(item, index) {
      this.bookmarksEditTempIndex = index;
      this.bookmarksEditForm = {
        title: "编辑书签",
        visible: true,
        name: item.name,
        url: item.url,
        icon: item.icon
      };
    },
    bookmarksDeleteSubmit(item, index) {
      this.bookmarksEdit.list.splice(index, 1);
      console.log(item, index);
    },
    async bookmarksIconFront() {
      try {
        const { data: res } = await axios.get(api.icon, {
          bookmarks: this.bookmarksEdit.list,
          user: sessionStorage.getItem("user").replace(/\"/g, "")
        });
        this.icon.visible = true;
        this.icon.data = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    iconNameGet(data) {
      this.bookmarksEditForm.icon = data;
      this.icon.visible = false;
    }
  },
};
</script>
<style scoped>
.bookmarks-main {
  min-height: 280px;
}
.bookmarks-data-row-main {
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
.slick_list_item_span {
  margin-left: 20px;
}
.slick_list_item_button {
  margin-right: 10px;
  margin-left: auto;
}
</style>
