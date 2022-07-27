<template>
  <v-alert
    v-if="saleConfirmed"
    dense
    dismissible
    outlined
    type="success"
    class="ma-3"
  >
    Sale confirmed for Product: {{ saleConfirmed }}
  </v-alert>
</template>
<script>
export default {
  name: "AlertSuccess",
  props: {
    saleConfirmed: {},
  },
};
</script>
