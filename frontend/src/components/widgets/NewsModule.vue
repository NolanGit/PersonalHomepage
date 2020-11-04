<template>
  <section>
    <el-row class="margin_bottom-medium">
      <div class="div-flex">
        <div style="text-align: left; flex-grow: 1">{{ newsData.title }}</div>
        <el-radio-group
          size="mini"
          v-model="newsDataCategory"
          v-if="newsData.chooseItems.length > 1"
          @change="categoryChoosed(newsDataCategory)"
        >
          <el-radio-button
            :id="singleValue"
            :label="singleValue"
            v-for="singleValue in newsData.chooseItems"
            :key="singleValue"
          ></el-radio-button>
        </el-radio-group>
      </div>
    </el-row>
    <div style="text-align: left">
      <div class="scrollbar-div" style="max-height: 300px">
        <div
          class="margin_bottom-mini"
          v-for="(link, i) in newsDataShow"
          :key="link"
        >
          <a style="color: #409eff; font-size: 14px">{{ i + 1 }}</a>
          <a>.</a>
          <el-link type="primary" :href="link.url">{{ link.name }} </el-link>
          <br />
        </div>
      </div>
    </div>
  </section>
</template>
<script>
export default {
  name: "newsModule",
  props: {
    newsData: {},
  },
  watch: {},
  data() {
    return {
      newsDataCategory: undefined,
      newsDataShow: undefined,
    };
  },
  methods: {
    categoryChoosed(newsDataCategory) {
      for (let x = 0; x < this.newsData.data.length; x++) {
        console.log(this.newsData.data[x]);
        console.log(this.newsData.data[x].title);
        if (this.newsData.data[x].title == newsDataCategory) {
          console.log(this.newsData.data[x].data);
          this.newsDataShow = this.newsData.data[x].data;
          return;
        }
      }
    },
  },
  mounted() {
    this.newsDataCategory = this.newsData.choose;
    this.newsDataShow = this.newsData.show;
    console.log(this.newsData);
  },
};
</script>
</style>
