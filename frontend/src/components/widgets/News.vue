<template>
  <section>
    <el-row v-for="singleDataSuite in cookedData" :key="singleDataSuite">
      <el-col :span="6" v-for="(value, key) in singleDataSuite" :key="key">
        <el-card>
          <!-- title area -->
          <el-row>
            <div>{{ key }}</div>
            <el-radio-group v-model="radio1" v-if="value.length > 1">
              <el-radio-button
                :label="singleValue.title"
                v-for="singleValue in value"
                :key="singleValue"
              ></el-radio-button>
            </el-radio-group>
          </el-row>
          <!-- content area -->
          <el-row>
            <div v-for="link in value[0].url" :key="link"></div>
            {{ link }}</el-row
          >
        </el-card>
      </el-col>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";

const api = {
  get: "/news/get",
};

export default {
  name: "news",
  watch: {},
  data() {
    return {
      rawData: [],
      cookedData: {},
    };
  },
  methods: {
    async get() {
      try {
        const { data: res } = await axios.post(api.get);
        this.rawData = res.data;
        const STEP = 4; // 每行有几个
        let temp1 = [];
        let count = 0;
        temp1.push({});
        for (let k in this.rawData) {
          if (count < STEP) {
            count += 1;
          } else {
            count = 0;
            temp1.push({});
            count += 1;
          }
          temp1[temp1.length - 1][k] = this.rawData[k];
        }
        this.cookedData = temp1;
        console.log(temp1);
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
    this.get();
    this.$emit("done");
  },
};
</script>
</style>
