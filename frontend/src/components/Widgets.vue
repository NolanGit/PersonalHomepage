<template>
  <div>
    <el-tabs
      v-model="widgetSuiteLabelActiveName"
      @tab-click="handleClick"
      stretch="true"
      style="
        padding-bottom: 30px;
        width: 70%;
        text-align: center;
        margin: 0 auto;
      "
      v-if="widgetSuiteLabels.length > 1"
    >
      <el-tab-pane
        v-for="singleWidgetSuite in widgetSuiteLabels"
        :label="singleWidgetSuite.name"
        :name="singleWidgetSuite.id"
        :key="singleWidgetSuite"
      ></el-tab-pane>
    </el-tabs>
    <el-row
      class="margin_bottom-large"
      v-for="(singleWidgetSuite, suiteIndex) in widgetSuite"
      :key="singleWidgetSuite"
    >
      <el-col
        :span="singleWidget.span"
        v-for="(singleWidget, index) in singleWidgetSuite"
        :key="singleWidget"
      >
        <transition name="el-zoom-in-top">
          <el-card
            shadow="hover"
            v-show="singleWidget.show"
            class="margin_left-medium margin_right-medium"
          >
            <weather
              style="height: 330px"
              v-if="singleWidget.name == 'weather'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.auto_update"
              @done="done(suiteIndex, index)"
            />
            <bookmarks
              style="height: 330px"
              v-if="singleWidget.name == 'bookmarks'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              @done="done(suiteIndex, index)"
            />
            <appMonitor
              style="height: 330px"
              v-if="singleWidget.name == 'app'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.auto_update"
              @done="done(suiteIndex, index)"
            />
            <gold
              style="height: 330px"
              v-if="singleWidget.name == 'gold'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.auto_update"
              @done="done(suiteIndex, index)"
            />
            <notes
              style="height: 330px"
              v-if="singleWidget.name == 'notes'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.auto_update"
              @done="done(suiteIndex, index)"
            />
            <translator
              style="height: 330px"
              v-if="singleWidget.name == 'translator'"
              @done="done(suiteIndex, index)"
            />
            <wallpapers
              style="height: 330px"
              v-if="singleWidget.name == 'wallpapers'"
              @done="done(suiteIndex, index)"
            />
            <stock
              style="height: 330px"
              v-if="singleWidget.name == 'stock'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.auto_update"
              @done="done(suiteIndex, index)"
            />
            <fund
              style="height: 330px"
              v-if="singleWidget.name == 'fund'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :buttons="singleWidget.buttons"
              :flush="singleWidget.auto_update"
              @done="done(suiteIndex, index)"
            />
            <news
              v-if="singleWidget.name == 'news'"
              :user_id="user_id"
              :widget_id="singleWidget.id"
              :flush="singleWidget.auto_update"
              @done="done(suiteIndex, index)"
            />
          </el-card>
        </transition>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import axios from "axios";
import weather from "./widgets/Weather.vue";
import bookmarks from "./widgets/Bookmarks.vue";
import appMonitor from "./widgets/AppMonitor.vue";
import gold from "./widgets/GoldPrice.vue";
import notes from "./widgets/Notes.vue";
import translator from "./widgets/Translator.vue";
import wallpapers from "./widgets/Wallpapers.vue";
import stock from "./widgets/Stock.vue";
import fund from "./widgets/Fund.vue";
import news from "./widgets/News.vue";

const api = {
  get: "/widget/get",
  suiteGet: "/widget/suite/get",
};

export default {
  name: "widgets",
  props: {
    user_id: Number,
  },
  components: {
    weather,
    bookmarks,
    appMonitor,
    gold,
    notes,
    translator,
    wallpapers,
    stock,
    fund,
    news,
  },
  watch: {
    user_id(newVal, oldVal) {
      this.widgetSuiteLabelGet();
    },
  },
  data() {
    return {
      widgetSuiteLabelActiveName: "",
      widgetSuiteLabels: [],
      widgetSuite: [],
      widget: [],
    };
  },
  methods: {
    async widgetSuiteLabelGet() {
      try {
        const { data: res } = await axios.post(api.suiteGet, {
          user_id: this.user_id,
        });

        this.widgetSuiteLabels = res.data;

        //这里有一个坑，当以数字作为el-tab-panel的name时，tab下方标识当前被触发tab的横条不能被正确计算并显示，所以要将el-tab-panel的name转化为字符串
        for (let x = 0; x < this.widgetSuiteLabels.length; x++) {
          this.widgetSuiteLabels[x].id = String(this.widgetSuiteLabels[x].id);
        }

        if (this.widgetSuiteLabels.length != 0) {
          this.widgetSuiteLabelActiveName = this.widgetSuiteLabels[0].id;
          this.widgetGet(this.widgetSuiteLabels[0].id);
        }
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    handleClick(activeTab) {
      this.widgetGet(activeTab.name);
    },
    async widgetGet(widgetSuiteLabelActiveId) {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
          widget_suite_id: Number(widgetSuiteLabelActiveId),
        });
        for (let x = 0; x < res.data.length; x++) {
          res.data[x].show = false;
          res.data[x].flush = false;
        }
        this.widget = res.data;
        await this.widgetSuiteGenerate();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    widgetSuiteGenerate() {
      var count = 0;
      this.widgetSuite = [];
      this.widgetSuite.push([]);
      for (let x = 0; x < this.widget.length; x++) {
        count += this.widget[x].span;
        if (count > 24) {
          this.widgetSuite.push([]);
          count = 0;
          count += this.widget[x].span
        }
        this.widgetSuite[this.widgetSuite.length - 1].push(this.widget[x]);
      }
    },
    done(suiteIndex, index) {
      this.widgetSuite[suiteIndex][index].show = true;
      this.widgetSuite[suiteIndex][index].flush = false;
    },
  },
  mounted() {
    this.widgetSuiteLabelGet();
  },
};
</script>
</style>
