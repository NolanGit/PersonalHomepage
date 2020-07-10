<template>
  <div>
    <el-tabs
      v-model="widgetSuiteLabelActiveName"
      @tab-click="handleClick"
      stretch="true"
      style="padding-bottom: 30px; width: 70%; text-align: center; margin: 0 auto;"
    >
      <el-tab-pane
        v-for="(singleWidgetSuite) in widgetSuiteLabels"
        :label="singleWidgetSuite.name"
        :name="singleWidgetSuite.id"
        :key="singleWidgetSuite"
      ></el-tab-pane>
    </el-tabs>
    <el-row
      class="margin_bottom-large"
      v-for="(singleWidgetSuite,suiteIndex) in widgetSuite"
      :key="singleWidgetSuite"
    >
      <el-col
        :span="singleWidget.span"
        v-for="(singleWidget,index) in singleWidgetSuite"
        :key="singleWidget"
      >
        <transition name="el-zoom-in-top">
          <el-card
            shadow="hover"
            v-show="singleWidget.show"
            class="margin_left-medium margin_right-medium"
          >
            <weather
              v-if="singleWidget.name=='weather'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.flush"
              @done="done(suiteIndex,index)"
            />
            <bookmarks
              v-if="singleWidget.name=='bookmarks'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              @done="done(suiteIndex,index)"
            />
            <appMonitor
              v-if="singleWidget.name=='app'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.flush"
              @done="done(suiteIndex,index)"
            />
            <gold
              v-if="singleWidget.name=='gold'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.flush"
              @done="done(suiteIndex,index)"
            />
          </el-card>
        </transition>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import axios from "axios";
import weather from "./Weather.vue";
import bookmarks from "./Bookmarks.vue";
import appMonitor from "./AppMonitor.vue";
import gold from "./Gold.vue";

const api = {
  get: "/widget/get",
  suiteGet: "/widget/suite/get"
};

export default {
  name: "widget",
  props: {
    user_id: Number
  },
  components: {
    weather,
    bookmarks,
    appMonitor,
    gold
  },
  data() {
    return {
      widgetSuiteLabelActiveName: "",
      widgetSuiteLabels: [],
      widgetSuite: [],
      widget: []
    };
  },
  methods: {
    async widgetSuiteLableGet() {
      try {
        const { data: res } = await axios.post(api.suiteGet, {
          user_id: this.user_id
        });
        this.widgetSuiteLabels = res.data;
        if (this.widgetSuiteLabels.length != 0) {
          this.widgetSuiteLabelActiveName = this.widgetSuiteLabels[0].name;
          this.widgetGet(this.widgetSuiteLabels[0].id);
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    handleClick(tab) {
      this.widgetGet(tab.name);
    },
    async widgetGet(widgetSuiteLabelActiveId) {
      try {
        // let widget_suite_id = 0;
        // for (let x = 0; x < this.widgetSuiteLabels.length; x++) {
        //   if (this.widgetSuiteLabels[x].name == widgetSuiteLabelActiveId) {
        //     widget_suite_id = this.widgetSuiteLabels[x].id;
        //     break;
        //   }
        // }
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
          widget_suite_id: widgetSuiteLabelActiveId
        });
        for (let x = 0; x < res.data.length; x++) {
          res.data[x].show = false;
          res.data[x].flush = false;
        }
        this.widget = res.data;
        this.widgetSuiteGenerate(this.autoUpdate);
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    widgetSuiteGenerate(autoUpdate) {
      var count = 0;
      this.widgetSuite = [];
      this.widgetSuite.push([]);
      for (let x = 0; x < this.widget.length; x++) {
        if (count >= 24) {
          this.widgetSuite.push([]);
          this.count = 0;
        }
        this.widgetSuite[this.widgetSuite.length - 1].push(this.widget[x]);
        count += this.widget[x].span;
      }
      autoUpdate();
    },
    autoUpdate() {
      for (let x = 0; x < this.widgetSuite.length; x++) {
        for (let y = 0; y < this.widgetSuite[x].length; y++) {
          window.setInterval(() => {
            setTimeout((this.widgetSuite[x][y].flush = true), 0);
          }, this.widgetSuite[x][y].auto_update);
        }
      }
    },
    done(suiteIndex, index) {
      this.widgetSuite[suiteIndex][index].show = true;
      this.widgetSuite[suiteIndex][index].flush = false;
    }
  },
  mounted() {
    this.widgetSuiteLableGet();
  }
};
</script>
</style>
