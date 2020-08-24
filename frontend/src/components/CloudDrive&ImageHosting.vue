<template>
  <section>
    <el-tabs
      v-model="activeFunction"
      @tab-click="handleClick"
      stretch="true"
      class="margin_bottom-small margin_left-medium margin_right-medium"
    >
      <el-tab-pane label="网盘" name="first"></el-tab-pane>
      <el-tab-pane label="图床" name="second"></el-tab-pane>
    </el-tabs>
    <CloudDrive v-if="activeFunction=='first'" :user_id="user_id" />
  </section>
</template>
<script>
import axios from "axios";
import CloudDrive from "./CloudDrive.vue";

const api = {
  download: "/download",
  get: "/cloudDrive/get",
  save: "/cloudDrive/save",
  share: "/cloudDrive/share/set",
  unShare: "/cloudDrive/share/cancel",
  delete: "/cloudDrive/delete",
};

export default {
  name: "CloudDriveAndImageHosting",
  props: {
    user_id: Number,
  },
  components: {
    CloudDrive,
  },
  watch: {},
  data() {
    return {
      activeFunction: "first",
    };
  },
  methods: {},
  mounted() {},
};
</script>
</style>
