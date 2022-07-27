<template>
  <v-alert
    v-if="failedOperation"
    dense
    dismissible
    outlined
    type="warning"
    class="ma-3"
  >
    {{ failedOperation }}
  </v-alert>
</template>
<script>
export default {
  name: "AlertError",
  props: {
    failedOperation: {},
  },
};
</script>
