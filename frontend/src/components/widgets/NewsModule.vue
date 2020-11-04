<template>
  <section>
    <el-row>
      <div class="div-flex">
        <div>{{ newsData.title }}</div>
        <el-radio-group
          size="mini"
          v-model="newsDatachoose"
          v-if="newsData.chooseItems.length > 1"
          @change="aaa(newsData.choose)"
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
    <el-row>
      <div class="scrollbar-div" style="max-height: 300px">
        <el-link
          type="primary"
          v-for="link in newsDataShow"
          :key="link"
          :href="link.url"
          >{{ link.name }}</el-link
        >
      </div>
    </el-row>
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
      newsDataChoose: undefined,
      newsDataShow: undefined,
    };
  },
  methods: {
    aaa(newsDatachoose) {
      for (let x = 0; x < this.newsData.data.length; x++) {
        if (this.newsData.data[x].title == newsDatachoose) {
          this.newsDataShow = this.newsData.data[x].data;
          return;
        }
      }
    },
  },
  mounted() {
    this.newsDatachoose = this.newsData.choose;
    this.newsDataShow = this.newsData.show;
    console.log(this.newsData);
  },
};
</script>
</style>
