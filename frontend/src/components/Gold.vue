<template>

</template>
<script>
import axios from "axios";
import Echarts from 'vue-echarts'
import 'echarts/lib/chart/line'
import 'echarts/lib/componet/title'
import 'echarts/lib/componet/tooltip'
import 'echarts/lib/componet/legent'
import WidgetButton from "./common/WidgetButton.vue";

const api = {
  goldData: "/gold/get",
};

export default {
  name: "gold",
  props: {
    user_id: Number,
    widget_id: Number,
    buttons: Array,
    flush: Boolean
  },
  components: {
    WidgetButton
  },
  watch: {
    flush(newVal, oldVal) {
      if (newVal) {
        this.weatherData();
      }
    }
  },
  data() {
  },
  methods: {
  },
  created() {},
  mounted() {
  }
};
</script>
</style>
