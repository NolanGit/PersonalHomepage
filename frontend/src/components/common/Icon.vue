<template>
  <div>
    <el-tabs v-model="iconCategory.active" type="card" @tab-click="changeCategory">
      <el-tab-pane label="全部" name="0"></el-tab-pane>
      <el-tab-pane
        v-for="singleIconCategory in iconCategory.data"
        :key="singleIconCategory"
        :label="singleIconCategory.name"
        :name="singleIconCategory.id"
      ></el-tab-pane>
    </el-tabs>
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
import axios from "axios";

const api = {
  icon: "/icon",
  iconCategory: "/iconCategory",
};
export default {
  name: "IconComponet",
  watch: {},
  data() {
    return {
      icons: [],
      iconsRaw: [],
      iconCategory: {
        active: "0",
        data: [],
      },
      iconData: [],
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
    },
    async iconGet() {
      try {
        const { data: res } = await axios.get(api.icon);
        this.iconsRaw = res.data;
        this.icons = this.iconsRaw;
        this.iconInit();
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    async iconCategoryGet() {
      try {
        const { data: res } = await axios.get(api.iconCategory);
        this.iconCategory.data = res.data;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    changeCategory(tab) {
      var category = Number(tab.name);
      if (tab.name == "0") {
        this.icons = this.iconsRaw;
        this.iconInit();
      } else {
        this.icons = [];
        for (let x = 0; x < this.iconsRaw.length; x++) {
          if (this.iconsRaw[x].category == category) {
            this.icons.push(this.iconsRaw[x]);
          }
        }
        this.iconInit();
      }
    },
  },
  mounted() {
    this.iconCategoryGet();
    this.iconGet();
  },
};
</script>
<style scoped>
.icon-medium {
  font-size: 20px;
}
</style>
