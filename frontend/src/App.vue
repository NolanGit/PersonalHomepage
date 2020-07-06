// 前端页面主入口
// 首先试图从cookie中恢复用户名、登录名、用户id以及用户密钥，如果cookie中没有，则置相关字段为空或0
// 接着调用一个userInfo接口，此接口的作用是：当存在cookie时，检查cookie的有效性。
// 如果cookie过期则清空cookie，置相关字段为空或0，获取不登陆状态可以使用的组件列表并加载；如果有效，则获取用户的组件并加载
<template>
  <div id="app">
    <githubConner />
    <el-row class="loginRow">
      <login :user_id="user_id" :user_name="user_name" :login_name="login_name" />
    </el-row>
    <el-row class="searchRow">
      <search :user_id="user_id" />
    </el-row>
    <div class="cardRow">
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
  </div>
</template>

<script>
import axios from "axios";
import githubConner from "./components/common/GithubConner";
import search from "./components/Search.vue";
import login from "./components/Login.vue";
import weather from "./components/Weather.vue";
import bookmarks from "./components/Bookmarks.vue";
import appMonitor from "./components/AppMonitor.vue";
import gold from "./components/Gold.vue";

const api = {
  userInfo: "/userInfo",
  widget: "/widget"
};

export default {
  components: {
    githubConner,
    search,
    login,
    weather,
    bookmarks,
    appMonitor,
    gold
  },
  data() {
    return {
      user: "",
      user_id: 0,
      widget: [],
      widgetSuite: [],
      flush: false
    };
  },
  methods: {
    async userInfo() {
      try {
        const { data: res } = await axios.post(api.userInfo, {
          user_id: this.user_id
        });
      } catch (e) {
        if (e.response.status == 401) {
          this.$cookies.remove("user_key");
          this.$cookies.remove("user_name");
          this.$cookies.remove("user_id");
          this.$cookies.remove("login_name");
          this.user = "";
          this.user_id = 0;
        } else if (e.response.status == 403) {
          console.log(e.response.data.msg);
        } else {
          this.$message({
            message: e.response.data.msg,
            type: "error"
          });
        }
      }
      this.userIdFlush();
      this.widgetGet(this.widgetSuiteGenerate);
    },
    async widgetGet(widgetSuiteGenerate) {
      try {
        const { data: res } = await axios.post(api.widget, {
          user_id: this.user_id
        });
        for (let x = 0; x < res.data.length; x++) {
          res.data[x].show = false;
          res.data[x].flush = false;
          res.data[x].flushCount = res.data[x].auto_update;
        }
        this.widget = res.data;
        widgetSuiteGenerate();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
    widgetSuiteGenerate() {
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
    },
    userIdFlush() {
      try {
        this.user_name =
          this.$cookies.get("user_name") == null
            ? ""
            : this.$cookies.get("user_name");
        this.user_id =
          this.$cookies.get("user_id") == null
            ? 0
            : this.$cookies.get("user_id");
        this.login_name =
          this.$cookies.get("login_name") == null
            ? ""
            : this.$cookies.get("login_name");
      } catch (error) {
        this.user_name = "";
        this.user_id = 0;
        this.login_name = "";
      }
    },
    done(suiteIndex, index) {
      this.widgetSuite[suiteIndex][index].show = true;
      this.widgetSuite[suiteIndex][index].flush = false;
      this.widgetSuite[suiteIndex][index].flushCount = this.widgetSuite[suiteIndex][index].auto_update;
      window.setInterval(() => {
        setTimeout((this.widgetSuite[suiteIndex][index].flush = true), 0);
      }, this.widgetSuite[suiteIndex][index].flushCount);
    }
  },
  created() {
    this.userIdFlush();
  },
  mounted() {
    this.userInfo();
  }
};
</script>

<style>
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
.cardRow {
  padding-top: 120px;
}
</style>
