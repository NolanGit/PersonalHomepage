<template>
  <div class="bookmarks-main">
    <el-main class="noPadding" style="height: 300px;">
      <el-row type="flex" justify="center">
        <div class="widget-label">书签</div>
      </el-row>

      <div class="bookmarks-data-row-main">
        <el-carousel height="198px" trigger="click" :autoplay="false" indicator-position="outside">
          <el-carousel-item v-for="bookmarksSuite in bookmarksSuites" :key="bookmarksSuite">
            <el-row
              class="margin_bottom-medium"
              v-for="bookmarksArray in bookmarksSuite"
              :key="bookmarksArray"
            >
              <el-col :span="6" v-for="bookmark in bookmarksArray" :key="bookmark">
                <el-button
                  class="bookmarks-main-button"
                  size="small"
                  @click="bookmarksClicked(bookmark.url)"
                >
                  <i :class="bookmark.icon" style="margin-right: 5px; font-size: 15px"></i>
                  {{bookmark.name}}
                </el-button>
              </el-col>
            </el-row>
          </el-carousel-item>
        </el-carousel>
      </div>
    </el-main>

    <el-footer height="31px" style="justify-content: center; display: flex;" v-if="user_id != 0">
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @sort="sort()"
        @notify="notify()"
      ></WidgetButton>
    </el-footer>

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
            <el-button size="small" @click="iconChoose()">选择图标</el-button>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="bookmarksEditFormConfirmClicked()">确定</el-button>
      </span>
    </el-dialog>

    <!--编辑顺序界面-->
    <el-dialog title="编辑书签" :visible.sync="bookmarksEdit.visible" width="40%">
      <SlickSort
        v-if="bookmarksEdit.visible"
        :list="bookmarksEdit.list"
        :can_be_edit="true"
        @submit="bookmarksEditSubmit"
        @edit="bookmarksSetting"
      ></SlickSort>
    </el-dialog>

    <!--选择图标界面-->
    <el-dialog title="选择喜欢的图标" :visible.sync="icon.visible" width="70%">
      <IconComponet @iconName="iconNameGet"></IconComponet>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
import IconComponet from "../common/Icon.vue";
import SlickSort from "../common/SlickSort.vue";
import WidgetButton from "../common/WidgetButton.vue";
import { deepClone } from "../../js/common";

const api = {
  get: "/bookmarks/get",
  bookmarksAdd: "/bookmarks/bookmarksAdd",
  bookmarksEdit: "/bookmarks/bookmarksEdit",
};
export default {
  name: "bookmarks",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
  },
  components: {
    IconComponet,
    SlickSort,
    WidgetButton,
  },
  data() {
    return {
      bookmarksDataRaw: [], //未处理的原始数据
      bookmarksSuites: [], //分组后的数据，原始数据
      bookmarksEdit: {
        visible: false,
        list: [],
      },
      bookmarksEditForm: {
        visible: false,
        name: "",
        url: "https://",
        icon: "",
      },
      bookmarksEditTempIndex: 0,
      icon: {
        visible: false,
      },
    };
  },
  methods: {
    bookmarksClicked(bookmarkUrl) {
      window.open(bookmarkUrl);
    },
    bookmarksSuitesGenerate() {
      const STEP1 = 4; // 每行有几个
      const STEP2 = 3; // 每页有几行
      let temp1 = [];
      let temp2 = [];
      for (let x = 0; x < this.bookmarksDataRaw.length; x += STEP1) {
        temp1.push([]);
        for (let y = 0; y < STEP1; y++) {
          if (this.bookmarksDataRaw[x + y] != undefined) {
            temp1[temp1.length - 1].push(this.bookmarksDataRaw[x + y]);
          }
        }
      }
      for (let x = 0; x < temp1.length; x += STEP2) {
        temp2.push([]);
        for (let y = 0; y < STEP2; y++) {
          temp2[temp2.length - 1].push(temp1[x + y]);
        }
      }
      this.bookmarksSuites = temp2;
    },
    async bookmarksGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.bookmarksDataRaw = res.data;
        this.bookmarksSuitesGenerate();
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async bookmarksEditFormConfirmClicked() {
      if (this.bookmarksEditForm.title == "新增书签") {
        try {
          const { data: res } = await axios.post(api.bookmarksAdd, {
            url: this.bookmarksEditForm.url,
            name: this.bookmarksEditForm.name,
            icon: this.bookmarksEditForm.icon,
            user_id: this.user_id,
          });
          this.$message({
            message: res["msg"],
            type: "success",
          });
          this.bookmarksGet();
        } catch (e) {
          console.log(e);
          this.$message({
            message: e.response.data.msg,
            type: "error",
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
    add() {
      this.bookmarksEditForm = {
        title: "新增书签",
        visible: true,
        name: "",
        url: "https://",
        icon: "",
      };
    },
    sort() {
      this.bookmarksEdit.list = deepClone(this.bookmarksDataRaw);
      this.bookmarksEdit.visible = true;
    },
    async bookmarksEditSubmit(list) {
      for (let x = 0; x < list.length; x++) {
        list[x].order = x + 1;
      }
      try {
        const { data: res } = await axios.post(api.bookmarksEdit, {
          bookmarks: list,
          user_id: this.user_id,
        });
        this.$message({
          message: res["msg"],
          type: "success",
        });
        this.bookmarksEdit.visible = false;
        this.bookmarksGet();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
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
        icon: item.icon,
      };
    },
    iconChoose() {
      this.icon.visible = true;
    },
    iconNameGet(data) {
      this.bookmarksEditForm.icon = data;
      this.icon.visible = false;
    },
  },
  mounted() {
    this.bookmarksGet();
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
</style>
