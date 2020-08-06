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
        <SlickList :lockToContainerEdges="true" class="list" lockAxis="y" v-model="item.itemArr">
          <SlickItem
            class="list-item"
            v-for="(item, index) in item.itemArr"
            :index="index"
            :key="index"
          >{{ item }}</SlickItem>
        </SlickList>
      </SlickItem>
    </SlickList>
  </div>
</template>
<script>
import axios from "axios";
import { SlickList, SlickItem } from "vue-slicksort";
const api = {
  get: "/widget/get",
  suiteGet: "/widget/suite/get",
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
      items: [
        {
          name: "title1",
          itemArr: ["Item1", "Item2", "Item3"],
        },
        {
          name: "title2",
          itemArr: ["Item4", "Item5", "Item6"],
        },
        {
          name: "title3",
          itemArr: ["Item7", "Item8", "Item9"],
        },
      ],
    };
  },
  methods: {},
  mounted() {},
};
</script>
<style scoped>
body,
html {
  -moz-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
h3,
h4 {
  text-align: center;
}
</style>
