<template>
  <div>
    <el-row v-for="iconsuite in icons" :key="iconsuite">
      <el-col :span="2" v-for="icon in iconsuite" :key="icon">
        <el-button size="small" @click="iconChoosed(icon.name)">
          <i :class="icon.name" style="margin-right=5px;font-size=15px"></i>选择
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
      this.iconData = newVal;
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
    }
  },
  mounted() {
    for (let x = 0; x < Math.floor(this.icons.length / 12); x++) {
      this.iconData.push([]);
      for (let y = 0; y < 12; y++) {
        this.iconData[this.iconData.length - 1].push(this.icons[x * 12 + y]);
      }
    }
    console.log(this.iconData);
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
