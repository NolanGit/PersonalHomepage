// 前端页面主入口
// 首先试图从cookie中恢复用户名、登录名、用户id以及用户密钥，如果cookie中没有，则置相关字段为空或0
// 接着调用一个userInfo接口，此接口的作用是：当存在cookie时，检查cookie的有效性。
// 如果cookie过期则清空cookie，置相关字段为空或0，获取不登陆状态可以使用的组件列表并加载；如果有效，则获取用户的组件并加载
<template>
  <div id="app" v-if="initial">
    <githubConner />
    <el-row class="loginRow">
      <login
        :user_id="user_id"
        :user_name="user_name"
        :login_name="login_name"
      />
    </el-row>
    <el-row class="searchRow">
      <search :user_id="user_id" />
    </el-row>
    <div class="cardRow">
      <widgets :user_id="user_id" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import githubConner from "./components/common/GithubConner";
import search from "./components/Search.vue";
import login from "./components/Login.vue";
import widgets from "./components/Widgets.vue";

const api = {
  userInfo: "/userInfo",
};

export default {
  components: {
    githubConner,
    search,
    login,
    widgets,
  },
  data() {
    return {
      initial: false,
      user_id: 0,
      widget: [],
      widgetSuite: [],
      flush: false,
      activeName: "second",
    };
  },
  methods: {
    async userInfo() {
      try {
        const { data: res } = await axios.post(api.userInfo, {
          user_id: this.user_id,
        });
        this.$cookies.set("csrf_token", res.data.csrf_token);
      } catch (e) {
        if (e.response.status == 401) {
          this.$cookies.remove("user_key");
          this.$cookies.remove("user_name");
          this.$cookies.remove("user_id");
          this.$cookies.remove("login_name");
        } else if (e.response.status == 403) {
          console.log(e.response.data.msg);
        } else {
          this.$message({
            message: e.response.data.msg,
            type: "error",
          });
        }
      }
      await this.userIdFlush();
      this.initial = true;
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
  },
  async created() {
    await this.userIdFlush();
  },
  async mounted() {
    await this.userInfo();
  },
};
</script>

<style>
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
.cardRow {
  padding-top: 80px;
}
</style>
