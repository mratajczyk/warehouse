<template>
  <v-dialog
    v-model="show"
    transition="dialog-top-transition"
    max-width="600"
    :retain-focus="false"
  >
    <template v-slot:default="dialog">
      <v-card>
        <v-toolbar color="primary" dark
          >Register sale #{{ item.product_id }}
        </v-toolbar>
        <v-card-text>
          <v-text-field
            label="Amount"
            v-model="saleAmount"
            hide-details
            :disabled="registerSalePending"
            single-line
            type="number"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="dialog.value = false">Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            class="ma-2"
            :loading="registerSalePending"
            :disabled="registerSalePending"
            color="secondary"
            @click="$emit('register', item.product_id, saleAmount)"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>
<script>
const DEFAULT_AMOUNT = 1;

export default {
  name: "SaleDialog",
  data: () => ({
    saleAmount: null,
    show: false,
  }),
  props: {
    registerSalePending: {
      type: Boolean,
      default: false,
    },
    item: {
      type: Object,
    },
  },
  mounted() {
    this.resetAmount();
  },
  methods: {
    resetAmount() {
      this.saleAmount = DEFAULT_AMOUNT;
    },
  },
  watch: {
    item: function () {
      this.show = !!this.item;
      this.resetAmount();
    },
  },
};
</script>
