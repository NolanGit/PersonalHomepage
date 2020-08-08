<template>
<section>
  <div class="margin_left-large">
    <SlickList
      :lockToContainerEdges="true"
      axis="x"
      lockAxis="x"
      v-model="items"
      class="SortableList"
      @input="getChangeLists"
      style="float: left;"
    >
      <SlickItem v-for="(item, index) in items" class="SortableItem" :index="index" :key="index">
        <el-row>
          <el-row class="div-flex margin_top-medium" style="margin-bottom: 30px;">
            <i
              class="el-icon-s-operation margin_right-medium margin_left-small"
              style="color: #6a6c70;"
            ></i>
            <p class="noMargin">{{ item.name }}</p>
            <div class="margin_left-large">
              <el-tooltip content="为组件集增加组件" placement="top">
                <el-button @click="widgetAdd(item)" size="mini" class="el-icon-plus"></el-button>
              </el-tooltip>
              <el-tooltip content="编辑组件集" placement="top">
                <el-button @click="widgetSuiteEdit(item)" size="mini" class="el-icon-setting"></el-button>
              </el-tooltip>
              <el-tooltip content="删除组件集" placement="top">
                <el-button
                  @click="widgetSuiteDelete(item)"
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
                v-for="(item, index) in item.widget_detail"
                :index="index"
                :key="index"
              >
                <i class="el-icon-s-operation" style="color: #6a6c70;"></i>
                <span class="slick_list_item_span">{{ item.name_zh }}</span>
                <div class="slick_list_item_button">
                  <el-tooltip content="删除组件" placement="top">
                    <el-button
                      @click="widgetDelete(item)"
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
        style="margin-top: 125px;"
      ></el-button>
    </el-tooltip>
  </div>
  
  </section>
</template>
<script>
import axios from "axios";
import { SlickList, SlickItem } from "vue-slicksort";
const api = {
  suiteDetail: "/widget/suite/detail",
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
    widgetAdd(item) {
      console.log(item);
    },
    widgetSuiteEdit(item) {
      console.log(item);
    },
    widgetSuiteDelete(item) {
      console.log(item);
    },
    widgetDelete(item) {
      console.log(item);
    },
    widgetSuiteAdd() {},
  },
  mounted() {
    this.widgetSuiteDetailGet();
  },
};
</script>
<style scoped>
</style>
