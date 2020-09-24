<template>
  <section>
    <el-carousel
      style="height: 100%;"
      trigger="click"
      :autoplay="false"
      indicator-position="outside"
    >
      <el-carousel-item v-for="wallpaper in wallpapersData" :key="wallpaper">
        <div>
          <img :src="wallpaper.url" class="image" />
          <div style="height: 30px; margin-top: 10px;">
            <b>{{'「'+wallpaper.date+'」'}}</b>
            <span>{{wallpaper.copyright}}</span>
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
  },
  mounted() {
    this.wallpapersGet();
  },
};
</script>
<style scoped>
.image {
  width: 90%;
  height: 100%;
  display: block;
}
.time {
  font-size: 13px;
  color: #999;
}
</style>
