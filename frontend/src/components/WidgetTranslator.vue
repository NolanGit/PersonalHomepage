<template>
  <section>
    <el-row>
      <el-col>
        <el-select size="mini" v-model="value" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
      <el-col>
        <i class="el-icon-refresh"></i>
      </el-col>
      <el-col>
        <el-select size="mini" v-model="value" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
      <el-col>
        <el-button size="mini" type="primary">主要按钮</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="textarea"></el-input>
      </el-col>
      <el-col>
        <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="textarea"></el-input>
      </el-col>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";

const api = {
  get: "/translator/get",
};

export default {
  name: "translator",
  watch: {},
  data() {
    return {
      options: [
        {
          value: "选项1",
          label: "黄金糕",
        },
        {
          value: "选项2",
          label: "双皮奶",
        },
        {
          value: "选项3",
          label: "蚵仔煎",
        },
        {
          value: "选项4",
          label: "龙须面",
        },
        {
          value: "选项5",
          label: "北京烤鸭",
        },
      ],
      value: "",
    };
  },
  methods: {},
  mounted() {},
};
</script>
</style>
