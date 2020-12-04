<template>
  <section>
    <el-row type="flex" justify="center">
      <div class="div-flex">
        <div class="widget-label">翻译</div>
        <i v-show="loading" class="el-icon-loading widget-label" style="padding-top: 3px;"></i>
      </div>
    </el-row>
    <el-row>
      <el-col :span="11">
        <el-select size="mini" v-model="fromLanguage" placeholder="请选择" style="width: 100%;" @change="translate()">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
      <el-col :span="2">
        <i
          class="el-icon-refresh"
          style="margin-top: 5px; cursor: pointer;"
          @click="exchangeLanguage()"
        ></i>
      </el-col>
      <el-col :span="11">
        <el-select size="mini" v-model="toLanguage" placeholder="请选择" style="width: 100%;" @change="translate()">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px; ">
      <el-col :span="11">
        <el-input
          style="min-height: 232px; max-height: 232px;"
          type="textarea"
          resize='none'
          :autosize="{ minRows: 10, maxRows: 10}"
          placeholder="请输入内容"
          v-model="rawText"
          @input="changed()"
        ></el-input>
      </el-col>
      <el-col :span="2">
        <i
          class="el-icon-refresh"
          style="margin-top: 5px; cursor: pointer;"
          @click="exchangeText()"
        ></i>
      </el-col>
      <el-col :span="11">
        <el-input
          style="min-height: 232px; max-height: 232px;"
          type="textarea"
          resize='none'
          :autosize="{ minRows: 10, maxRows: 10}"
          placeholder
          v-model="translatedText"
        ></el-input>
      </el-col>
    </el-row>
  </section>
</template>
<script>
import axios from "axios";

const api = {
  translate: "/translator/translate",
};

export default {
  name: "translator",
  watch: {},
  data() {
    return {
      loading: false,
      options: [
        { value: "zh", label: "简体中文" },
        { value: "en", label: "英语" },
        { value: "ru", label: "俄语" },
        { value: "es", label: "西班牙语" },
        { value: "fr", label: "法语" },
        { value: "ar", label: "阿拉伯语" },
        { value: "tr", label: "土耳其语" },
        { value: "pt", label: "葡萄牙语" },
        { value: "it", label: "意大利语" },
        { value: "th", label: "泰语" },
        { value: "id", label: "印度尼西亚语" },
        { value: "vi", label: "越南语" },
      ],
      fromLanguage: "zh",
      toLanguage: "en",
      rawText: "",
      translatedText: "",
    };
  },
  methods: {
    exchangeLanguage() {
      var _temp = this.fromLanguage;
      this.fromLanguage = this.toLanguage;
      this.toLanguage = _temp;
      this.translate();
    },
    exchangeText() {
      var _temp = this.rawText;
      this.rawText = this.translatedText;
      this.translatedText = _temp;
      this.translate();
    },
    changed() {
      clearTimeout(this.timer);
      this.timer = setTimeout(this.translate, 500);
    },
    async translate() {
      if (
        this.rawText == undefined ||
        this.rawText == "" ||
        this.rawText == null
      ) {
        return;
      }
      try {
        this.loading = true;
        const { data: res } = await axios.post(api.translate, {
          to_language: this.toLanguage,
          text: this.rawText,
        });
        this.translatedText = res.data;
        this.loading = false;
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error",
        });
        this.loading = false;
      }
    },
  },
  mounted() {
    this.$emit("done");
  },
};
</script>
</style>
