<template>
  <div class="search">
    <div>
      <i :class="searchIcon"></i>
    </div>
    <div>
      <el-input
        placeholder="请输入内容"
        v-model="word"
        @keyup.enter.native="search()"
        class="search-input"
      >
        <el-select
          class="search-engine-select"
          v-model="searchEngines.select"
          slot="prepend"
          placeholder="请选择"
        >
          <el-option
            v-for="item in searchEngines.options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
        <el-button class="search-button" slot="append" icon="el-icon-search" @click="search()"></el-button>
      </el-input>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Router from "vue-router";
import { searchEnginesData } from "../api/search";

export default {
  name: "search",
  data() {
    return {
      word: "",
      searchIcon: "search-icon el-icon-search",
      searchEngines: {
        select: "",
        options: []
      }
    };
  },
  methods: {
    searchEnginesDataFront() {
      searchEnginesData().then(data => {
        console.log(data);
        for (let s = 0; s < data.data.length; s++) {
          this.searchEngines.options.push({
            id: data.data[s].id,
            main_url: data.data[s].main_url,
            auto_complete_url: data.data[s].auto_complete_url,
            icon: data.data[s].icon,
            label: data.data[s].name,
            value: data.data[s].name
          });
        }
        this.searchEngines.select = this.searchEngines.options[0].value;
      });
    },
    search() {
      for (var s = 0; s < this.searchEngines.options.length; s++) {
        if (this.searchEngines.options[s].value == this.searchEngines.select) {
          break;
        }
      }
      var searchUrl = this.searchEngines.options[s].main_url.replace(
        "%word%",
        this.word
      );
      window.open(searchUrl);
    }
  },
  created() {
    this.searchEnginesDataFront();
  }
};
</script>
<style scoped>
.search-icon {
  font-size: 100px;
  padding-top: 60px;
  padding-bottom: 60px;
}
.search-input {
  margin-left: 50px;
  margin-right: 50px;
  max-width: 50%;
}
.search-engine-select {
  width: 120px;
}
.search-button {
  width: 70px;
}
</style>
