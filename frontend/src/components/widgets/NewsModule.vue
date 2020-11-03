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
            :label="singleValue.title"
            v-for="singleValue in newsData.chooseItems"
            :key="singleValue.title"
          ></el-radio-button>
        </el-radio-group>
      </div>
    </el-row>
    <el-row style="height: 300px">
      <el-link type="primary" v-for="link in newsData.show" :key="link">{{
        link.name
      }}</el-link>
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
  methods: {},
  mounted() {},
};
</script>
</style>
