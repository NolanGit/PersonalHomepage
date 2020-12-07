<template>
  <section>
    <el-carousel
      style="height: 100%; overflow-y: hidden"
      trigger="click"
      :autoplay="true"
      :interval="5000"
      indicator-position="outside"
    >
      <el-carousel-item v-for="wallpaper in wallpapersData" :key="wallpaper">
        <div>
          <img
            @click="open(wallpaper.url)"
            :src="wallpaper.url"
            class="image"
          />
          <div style="height: 30px; margin-top: 10px">
            <!-- <b class="better_font_style" style="font-size: 15px;">{{'「'+wallpaper.date+'」'}}</b> -->
            <span class="better_font_style" style="font-size: 15px">{{
              wallpaper.copyright
            }}</span>
            <span
              @click="open(wallpaper.copyrightlink)"
              style="
                color: #409eff;
                font-size: 15px;
                cursor: pointer;
                margin-left: 10px;
              "
              >了解更多</span
            >
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </section>
</template>
<script>
import axios from "axios";

const api = {
  get: "/wallpapers/get",
};
export default {
  name: "wallpapers",
  data() {
    return {
      wallpapersData: [],
    };
  },
  methods: {
    async wallpapersGet() {
      try {
        const { data: res } = await axios.get(api.get);
        this.wallpapersData = res.data;
        this.$emit("done");
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
      }
    },
    open(url) {
      window.open(url);
    },
  },
  mounted() {
    this.wallpapersGet();
  },
};
</script>
<style scoped>
.image {
  max-height: 245px;
  object-fit: cover;
  cursor: pointer;
  box-shadow: 3px 3px 2px rgba(0, 0, 0, 0.5);
}
</style>
