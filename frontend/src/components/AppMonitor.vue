<template>
  <section>
    <el-row type="flex" justify="center">
      <div>
        <div class="widget-label">APP</div>
      </div>
    </el-row>
    <el-carousel height="180px" trigger="click" interval="5000" indicator-position="outside">
      <el-carousel-item v-for="appData in appSuite" :key="appData">
        <el-table :data="appData" style="width: 100%" size="mini">
          <el-table-column prop="date" label="名称"></el-table-column>
          <el-table-column prop="name" label="当前价格" width="80"></el-table-column>
        </el-table>
      </el-carousel-item>
    </el-carousel>
    <el-row type="flex" justify="center" class="margin-top-medium" v-show="user!=undefined">
      <el-button
        class="margin_left-mini margin_right-mini"
        size="small"
        @click="bookmarksOptionButtonAddClicked()"
        icon="el-icon-plus"
        circle
      ></el-button>
      <el-button
        class="bmargin_left-mini margin_right-mini"
        size="small"
        @click="bookmarksOptionButtonSettingClicked()"
        icon="el-icon-setting"
        circle
      ></el-button>
    </el-row>
  </section>
</template>

<script>
import axios from "axios";
const api = {
  get: "/app/get",
  add: "/app/add",
  edit: "/app/edit"
};
export default {
  name: "AppMonitor",
  props: {
    user: String,
    userID: String
  },
  components: {},
  data() {
    return {
      appSuite: []
    };
  },
  methods: {
    async appGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.userID
        });
        const STEP = 4; // 每页几行
        let temp = [];
        for (let x = 0; x < this.res.data.length; x += STEP) {
          temp.push([]);
          for (let y = 0; y < STEP; y++) {
            if (this.res.data[x + y] != undefined) {
              temp[temp.length - 1].push(this.res.data[x + y]);
            }
          }
        }
        console.log(temp);
        this.appSuite = temp;
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    }
  },
  mounted() {
    this.appGet();
  }
};
</script>

<style scoped>
.noMargin {
  margin: 0;
}
</style>