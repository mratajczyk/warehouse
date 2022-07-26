<template>
  <v-card class="mx-auto">
    <v-card-title class="display-1">📦 Warehouse Application</v-card-title>
    <v-divider class="mx-4"></v-divider>
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
    <v-row class="pa-6">
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search Product"
        single-line
        hide-details
      ></v-text-field>
    </v-row>
    <v-data-table
      :headers="headers"
      :items="products"
      :items-per-page="10"
      :loading="tableLoading"
      class="elevation-0"
      :search="search"
    >
      <template v-slot:[`item.actions`]="{ item }">
        <v-dialog
          v-model="saleDialog"
          transition="dialog-top-transition"
          max-width="600"
          :retain-focus="false"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-row justify="end">
              <v-btn color="primary" v-bind="attrs" v-on="on" small class="mr-5"
                >SALE</v-btn
              >
            </v-row>
          </template>
          <template v-slot:default="dialog">
            <v-card>
              <v-toolbar color="primary" dark
                >Register sale #{{ item.product_id }}</v-toolbar
              >
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
                  @click="registerSale(item.product_id)"
                >
                  Confirm
                </v-btn>
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import http_proxy from "@/http_proxy";

const FAILED_TABLE_LOADING = "Loading Products failed, please wait";
const FAILED_SALE_NOT_AVALIABLE_PRODUCT =
  "Product not available for sale at the moment";
const FAILED_SALE = "Sale failed: ";
const DEFAULT_SALE_AMOUNT = 1;

export default {
  name: "ManageProducts",
  data: () => ({
    saleAmount: DEFAULT_SALE_AMOUNT,
    saleDialog: false,
    registerSalePending: false,
    failedOperation: null,
    saleConfirmed: null,
    tableLoading: false,
    search: "",
    headers: [
      { text: "SKU", value: "product_id" },
      { text: "Name", value: "name" },
      { text: "Stock", value: "stock" },
      { text: "", value: "actions", sortable: false },
    ],
    products: [],
  }),
  mounted() {
    this.loadStock();
  },
  methods: {
    showError(error_text) {
      this.failedOperation = error_text;
    },
    clearError() {
      this.failedOperation = null;
    },
    closeSaleDialog() {
      this.saleDialog = false;
    },
    resetSaleAmount() {
      this.saleAmount = DEFAULT_SALE_AMOUNT;
    },
    confirmSale(product_id) {
      this.saleConfirmed = product_id;
    },
    clearConfirmSale() {
      this.saleConfirmed = null;
    },
    startSalePending() {
      this.clearConfirmSale();
      this.registerSalePending = true;
    },
    stopSalePending() {
      this.registerSalePending = false;
    },
    registerSale(product_id) {
      this.startSalePending();
      http_proxy()
        .post(`/products/${product_id}/sale`, { amount: this.saleAmount })
        .then(() => {
          this.loadStock();
          this.confirmSale(product_id);
          this.clearError();
        })
        .catch((error) => {
          if (error.response.status === 422) {
            this.showError(
              FAILED_SALE + JSON.stringify(error.response.data.errors.json)
            );
          }
          if (error.response.status === 404) {
            this.showError(FAILED_SALE_NOT_AVALIABLE_PRODUCT);
          }
        })
        .finally(() => {
          setTimeout(() => {
            {
              this.resetSaleAmount();
              this.closeSaleDialog();
              this.stopSalePending();
            }
          }, 1000);
        });
    },
    loadStock() {
      this.tableLoading = true;
      http_proxy()
        .get(`/products`)
        .then((response) => {
          this.products = response.data.products;
          this.clearError();
        })
        .catch(() => {
          this.products = [];
          this.showError(FAILED_TABLE_LOADING);
          setTimeout(() => {
            this.loadStock();
          }, 1000);
        })
        .finally(() => {
          this.tableLoading = false;
        });
    },
  },
};
</script>
