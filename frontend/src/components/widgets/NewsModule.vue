<template>
  <section>
    <el-row>
      <div class="div-flex">
        <div>{{ newsData.title }}</div>
        <el-radio-group
          size="mini"
          v-model="newsData.choose"
          v-if="newsData.chooseItems.length > 1"
          @change="aaa()"
        >
          <el-radio-button
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
    return {};
  },
  methods: {
    aaa(x) {
      console.log(x);
    },
  },
  mounted() {},
};
</script>
</style>
