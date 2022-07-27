<template>
  <v-dialog
    v-model="show"
    transition="dialog-top-transition"
    max-width="600"
    :retain-focus="false"
  >
    <template>
      <v-card>
        <v-toolbar color="primary" dark>Register sale #{{ itemId }} </v-toolbar>
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
          <v-btn text @click="$emit('cancel_dialog')">Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            class="ma-2"
            :loading="registerSalePending"
            :disabled="registerSalePending"
            color="secondary"
            @click="$emit('register', itemId, saleAmount)"
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
    show: true,
  }),
  props: {
    registerSalePending: {
      type: Boolean,
      default: false,
    },
    itemId: {
      type: String,
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
