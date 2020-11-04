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
          <el-radio
            :id="singleValue"
            :label="singleValue"
            v-for="singleValue in newsData.chooseItems"
            :key="singleValue"
          ></el-radio>
        </el-radio-group>
      </div>
    </el-row>
    <el-row>
      <div class="scrollbar-div" style="max-height: 300px">
        <el-link
          type="primary"
          v-for="link in newsData.show"
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
      newsDatachoose: undefined,
      //   newsData: {
      //     title: "百度",
      //     choose: "百度实时热点",
      //     chooseItems: ["百度实时热点", "百度今日热点", "百度七日热点"],
      //   },
    };
  },
  methods: {
    aaa(x) {
      console.log(x);
    },
  },
  mounted() {
    console.log(this.newsData);
  },
};
</script>
</style>
