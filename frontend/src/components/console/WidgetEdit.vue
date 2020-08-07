<template>
  <div>
    <SlickList
      :lockToContainerEdges="true"
      axis="x"
      lockAxis="x"
      v-model="items"
      class="SortableList"
      @input="getChangeLists"
    >
      <SlickItem v-for="(item, index) in items" class="SortableItem" :index="index" :key="index">
        {{ item.name }}
        <SlickList
          :lockToContainerEdges="true"
          class="list"
          lockAxis="y"
          v-model="item.widget_detail"
        >
          <SlickItem
            class="list-item"
            v-for="(item, index) in item.widget_detail"
            :index="index"
            :key="index"
          >{{ item.name_ch }}</SlickItem>
        </SlickList>
      </SlickItem>
    </SlickList>
  </div>
</template>
<script>
import axios from "axios";
import { SlickList, SlickItem } from "vue-slicksort";
const api = {
  suiteDetail: "/widget/suite/detail",
};

export default {
  name: "widgetEdit",
  props: {
    user_id: Number,
  },
  components: {
    SlickItem,
    SlickList,
  },
  watch: {},
  data() {
    return {
      items: [],
    };
  },
  methods: {
    async widgetSuiteDetailGet() {
      try {
        const { data: res } = await axios.post(api.suiteDetail, {
          user_id: this.user_id,
        });
        this.items = res.data;
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
    this.widgetSuiteDetailGet();
  },
};
</script>
<style scoped>
</style>
