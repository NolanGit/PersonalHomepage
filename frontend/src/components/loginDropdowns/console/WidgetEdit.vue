<template>
  <section class="scrollbar-div" style="max-height: 50vh">
    <el-row class="margin_left-large">
      <p
        class="notesText"
        style="
          font-size: 12px;
          color: #f56c6c;
          padding-top: 0px;
          margin-top: 0px;
          margin-bottom: 10px;
        "
      >
        *拖动以排序
      </p>
      <SlickList
        :lockToContainerEdges="true"
        axis="x"
        lockAxis="x"
        v-model="items"
        class="SortableList"
        @input="getChangeLists"
        style="float: left"
      >
        <SlickItem
          v-for="(item, index) in items"
          class="SortableItem"
          :index="index"
          :key="index"
        >
          <el-row>
            <el-row
              class="div-flex margin_top-medium"
              style="margin-bottom: 30px"
            >
              <i
                class="el-icon-s-operation margin_right-medium margin_left-small"
                style="color: #6a6c70; margin-top: 3px"
              ></i>
              <p class="noMargin">{{ item.name }}</p>
              <div class="margin_left-large">
                <el-tooltip content="编辑组件集名称" placement="top">
                  <el-button
                    @click="widgetSuiteEdit(index)"
                    size="mini"
                    class="el-icon-edit"
                  ></el-button>
                </el-tooltip>
                <el-tooltip content="为组件集增加组件" placement="top">
                  <el-button
                    @click="widgetAdd(index)"
                    size="mini"
                    class="el-icon-plus"
                  ></el-button>
                </el-tooltip>
                <el-tooltip content="删除组件集" placement="top">
                  <el-button
                    @click="widgetSuiteDelete(item, index)"
                    type="danger"
                    size="mini"
                    class="el-icon-delete"
                  ></el-button>
                </el-tooltip>
              </div>
            </el-row>
            <el-row>
              <SlickList
                :lockToContainerEdges="true"
                class="list"
                lockAxis="y"
                v-model="item.widget_detail"
              >
                <SlickItem
                  class="list-item"
                  v-for="(widgetItem, widgetIndex) in item.widget_detail"
                  :index="widgetIndex"
                  :key="widgetIndex"
                >
                  <i class="el-icon-s-operation" style="color: #6a6c70"></i>
                  <span class="slick_list_item_span">{{
                    widgetItem.name_zh
                  }}</span>
                  <div class="slick_list_item_button">
                    <el-tooltip content="删除组件" placement="right">
                      <el-button
                        @click="widgetDelete(index, widgetItem, widgetIndex)"
                        type="danger"
                        size="mini"
                        class="el-icon-delete"
                      ></el-button>
                    </el-tooltip>
                  </div>
                </SlickItem>
              </SlickList>
            </el-row>
          </el-row>
        </SlickItem>
      </SlickList>
      <el-tooltip content="增加组件集" placement="top">
        <el-button
          @click="widgetSuiteAdd()"
          circle
          class="el-icon-plus margin_left-large"
          style="margin-top: 125px"
        ></el-button>
      </el-tooltip>
    </el-row>
    <el-row class="margin_left-large">
      <el-button
        @click="submit()"
        type="primary"
        size="small"
        class="margin_top-medium"
        >提交</el-button
      >
    </el-row>

    <el-drawer
      :title="edit.title"
      :visible.sync="edit.visible"
      size="60%"
      direction="btt"
      @closed="editFormClosed"
    >
      <div
        class="div-flex margin_bottom-medium margin_left-large scrollbar-div"
        style="max-height: 50vh"
        v-if="edit.action == 'editWidgetSuite'"
      >
        <div class="td__p--label td--label">请输入组件集名称：</div>
        <el-input
          class="width--medium margin_right-small"
          v-model="edit.widgetSuiteName"
          size="small"
          placeholder="请输入"
        ></el-input>
        <el-button type="primary" size="mini" plain @click="widgetSuiteEdited()"
          >确定</el-button
        >
      </div>
      <div class="scrollbar-div margin_left-medium margin_bottom-medium" style="width: 500px; max-height: 50vh">
        <el-table
          v-if="edit.action == 'addWidget'"
          :key="Math.random()"
          size="mini"
          :data="widgets"
          stripe
          style="width: 100%"
        >
          <el-table-column
            :key="Math.random()"
            prop="id"
            label="ID"
            :v-show="false"
          ></el-table-column>
          <el-table-column
            :key="Math.random()"
            prop="name_zh"
            label="名称"
          ></el-table-column>
          <el-table-column :key="Math.random()" label="操作" width="120">
            <template slot-scope="scope">
              <el-button
                class="noMargin"
                type="primary"
                size="mini"
                plain
                @click="widgetAdded(scope.row)"
                >选择</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-drawer>
  </section>
</template>
<script>
import axios from "axios";
import { SlickList, SlickItem } from "vue-slicksort";

const api = {
  suiteDetail: "/widget/suite/detail",
  suiteSave: "/widget/suite/save",
  widgetAll: "widget/get_all",
};

export default {
  name: "widgetEdit",
  props: {
    user_id: Number,
  },
  components: {
    SlickItem,
    SlickList,
  },
  watch: {},
  data() {
    return {
      items: [],
      widgets: [],
      edit: {
        visible: false,
        action: "",
        widgetSuiteIndexInOpration: "",
        widgetSuiteName: "",
      },
    };
  },
  methods: {
    async widgetSuiteDetailGet() {
      try {
        const { data: res } = await axios.post(api.suiteDetail, {
          user_id: this.user_id,
        });
        this.items = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async widgetAllGet() {
      try {
        const { data: res } = await axios.post(api.widgetAll);
        this.widgets = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    widgetAdd(index) {
      this.widgetAllGet();
      this.edit.title = "添加小组件";
      this.edit.action = "addWidget";
      this.edit.widgetSuiteIndexInOpration = index;
      this.edit.visible = true;
    },
    widgetAdded(item) {
      let widgetSuiteIndex = this.edit.widgetSuiteIndexInOpration;
      this.items[widgetSuiteIndex].widget_detail.push({
        id: item.id,
        name_zh: item.name_zh,
      });
      this.edit.visible = false;
    },
    widgetSuiteEdit(index) {
      this.edit.title = "编辑组件集名称";
      this.edit.action = "editWidgetSuite";
      this.edit.widgetSuiteIndexInOpration = index;
      this.edit.widgetSuiteName = this.items[index].name;
      this.edit.visible = true;
    },
    widgetSuiteDelete(item, index) {
      this.$confirm("确认删除[" + item.name + "]吗?", "提示", {}).then(
        async () => {
          this.items.splice(index, 1);
        }
      );
    },
    widgetDelete(index, widgetItem, widgetIndex) {
      this.$confirm("确认删除[" + widgetItem.name_zh + "]吗?", "提示", {}).then(
        async () => {
          this.items[index].widget_detail.splice(widgetIndex, 1);
          for (let x = 0; x < this.items[index].widget_detail; x++) {
            if (this.items[index].detail[x] == widgetItem.id) {
              this.items[index].detail.splice(x, 1);
            }
          }
        }
      );
    },
    widgetSuiteAdd() {
      this.edit.title = "新增组件集";
      this.edit.action = "editWidgetSuite";
      this.edit.visible = true;
    },
    widgetSuiteEdited() {
      if (this.edit.title == "新增组件集") {
        this.items.push({
          name: this.edit.widgetSuiteName,
          detail: [],
          widget_detail: [],
        });
      } else if (this.edit.title == "编辑组件集名称") {
        let widgetSuiteIndex = this.edit.widgetSuiteIndexInOpration;
        this.items[widgetSuiteIndex].name = this.edit.widgetSuiteName;
      }
      this.edit.visible = false;
    },
    editFormClosed() {
      this.edit.widgetSuiteName = "";
    },
    async submit() {
      for (let x = 0; x < this.items.length; x++) {
        this.items[x].order = x;
        this.items[x].detail = [];
        for (let y = 0; y < this.items[x].widget_detail.length; y++) {
          this.items[x].detail.push(this.items[x].widget_detail[y].id);
        }
      }
      try {
        const { data: res } = await axios.post(api.suiteSave, {
          user_id: this.user_id,
          suite_data: this.items,
        });
        this.$message({
          message: res.msg,
          type: "success",
        });
        location.reload();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
  },
  mounted() {
    this.widgetSuiteDetailGet();
  },
};
</script>
<style scoped>
</style>
