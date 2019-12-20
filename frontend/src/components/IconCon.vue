<template>
  <div>
    <el-button v-for="icon in iconData" :key="icon" :icon="icon"></el-button>
  </div>
</template>
<script>

export default {
  name: "IconComponet",
  props: {
    icons: Array
  },
  watch: {
    icons(newVal, oldVal) {
      console.log(newVal);
      this.iconData = newVal;
    }
  },
  data() {
    return {
      iconData: []
    };
  },
  methods: {},
  created() {},
  mounted() {}
};
</script>
<style scoped>
.text-mini {
  font-size: 10px;
}
.text-small {
  font-size: 14px;
}
.text-medium {
  font-size: 20px;
}
.margin_right-small {
  margin-right: 10px;
}
.margin_left-medium {
  margin-left: 20px;
}
.margin_bottom-medium {
  margin-bottom: 20px;
}
.margin_bottom-large {
  margin-bottom: 40px;
}
.margin-top-medium {
  margin-top: 20px;
}
</style>
