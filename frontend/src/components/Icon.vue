<template>
  <div>
    <div v-for="icon in icons" :key="icon">
      <el-button>
        <i :class="icon.name" style="margin-right=5px;font-size=15px"></i>选择
      </el-button>
    </div>
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
      iconData: [
        {
          id: 1,
          name: "iconfont icon-tianmaochaoshigouwuche"
        }
      ]
    };
  },
  methods: {},
  created() {},
  mounted() {
    this.iconData = this.icons;
    console.log(this.icons);
  }
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
