<template>
  <v-app>
    <v-main class="pa-12">
      <ManageProducts />
    </v-main>
  </v-app>
</template>

<script>
import ManageProducts from "./components/ManageProducts";

export default {
  name: "App",
  components: {
    ManageProducts,
  },
};
</script>
