<template>
  <div>
    <el-row v-for="iconsuite in iconData" :key="iconsuite" class="margin_bottom-medium">
      <el-col :span="2" v-for="icon in iconsuite" :key="icon">
        <el-button size="medium" @click="iconChoosed(icon.name)">
          <i :class="icon.name + ' icon-medium'"></i>
        </el-button>
      </el-col>
    </el-row>
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
      this.iconInit();
    }
  },
  data() {
    return {
      iconData: []
    };
  },
  methods: {
    iconChoosed(iconName) {
      this.$emit("iconName", iconName);
    },
    iconInit() {
      this.iconData = [];
      for (let x = 0; x < Math.floor(this.icons.length / 12) + 1; x++) {
        this.iconData.push([]);
        for (let y = 0; y < 12; y++) {
          if (
            x == Math.floor(this.icons.length / 12) &&
            y == this.icons.length % 12
          ) {
            break;
          }
          this.iconData[this.iconData.length - 1].push(this.icons[x * 12 + y]);
        }
      }
    }
  },
  mounted() {
    this.iconInit();
  }
};
</script>
<style scoped>
.icon-medium {
  font-size: 20px;
}
</style>
