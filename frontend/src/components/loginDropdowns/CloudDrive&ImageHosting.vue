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
    <CloudDrive
      v-if="activeFunction=='first'"
      :user_id="user_id"
      @cloudStatusChanged="cloudStatusChanged"
    />
    <ImageHosting
      v-if="activeFunction=='second'"
      :user_id="user_id"
      @cloudStatusChanged="cloudStatusChanged"
    />
  </section>
</template>
<script>
import axios from "axios";
import CloudDrive from "./CloudDrive.vue";
import ImageHosting from "./ImageHosting.vue";

export default {
  name: "CloudDriveAndImageHosting",
  props: {
    user_id: Number,
  },
  components: {
    CloudDrive,
    ImageHosting,
  },
  watch: {},
  data() {
    return {
      activeFunction: "first",
    };
  },
  methods: {
    cloudStatusChanged(cloudStatus) {
      this.$emit("cloudStatusChanged", cloudStatus);
    },
  },
  mounted() {},
};
</script>
</style>
