<template>
  <section>
    <el-row type="flex" justify="center">
      <div>
        <div class="widget-label">便签</div>
      </div>
    </el-row>
    <el-tabs tab-position="left" class="scrollbar-div" style="max-height: 210px;">
      <el-tab-pane
        v-for="singleNotesData in notesData"
        :key="singleNotesData"
        :label="singleNotesData.name"
      >
        <p
          style="color: #606266; font-size: 12px; font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;"
        >{{singleNotesData.content}}</p>
      </el-tab-pane>
    </el-tabs>
    <el-row type="flex" justify="center" v-show="user_id!=0">
      <WidgetButton
        :user_id="user_id"
        :widget_id="widget_id"
        :buttons="buttons"
        @add="add()"
        @sort="sort()"
        @notify="notify()"
        @setting="setting()"
      ></WidgetButton>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";
import WidgetButton from "./common/WidgetButton.vue";

const api = {
  get: "/notes/get",
};
export default {
  name: "notes",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
  },
  components: {
    WidgetButton,
  },
  data() {
    return {
      notesData: [],
    };
  },
  methods: {
    async notesGet() {
      try {
        const { data: res } = await axios.post(api.get, {
          user_id: this.user_id,
        });
        this.notesData = res.data;
        this.$emit("done");
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
    this.notesGet();
  },
};
</script>
<style scoped>
</style>
