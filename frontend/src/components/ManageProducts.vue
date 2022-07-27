<template>
  <div>
    <SaleDialog
      v-if="saleItem"
      :item-id="saleItem"
      :register-sale-pending="registerSalePending"
      @register="registerSale"
      @cancel_dialog="stopSaleDialog"
    />
    <v-card class="mx-auto">
      <v-card-title class="display-1">📦 Warehouse Application</v-card-title>
      <v-divider class="mx-4"></v-divider>
      <AlertError :failed-operation="failedOperation" />
      <AlertSuccess :sale-confirmed="saleConfirmed" />
      <v-data-table
        :headers="headers"
        :items="products"
        :items-per-page="10"
        :loading="tableLoading"
        class="elevation-1"
        :search="search"
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-row justify="end">
            <v-btn
              color="primary"
              small
              class="mr-5"
              @click="startSaleDialog(item.product_id)"
              >SALE</v-btn
            >
          </v-row>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import http_proxy from "@/http_proxy";

import AlertError from "@/components/AlertError";
import AlertSuccess from "@/components/AlertSuccess";
import SaleDialog from "@/components/SaleDialog";

const FAILED_TABLE_LOADING = "Loading Products failed, please wait";
const FAILED_SALE_NOT_AVAILABLE_PRODUCT =
  "Product not available for sale at the moment";
const FAILED_SALE = "Sale failed: ";

export default {
  name: "ManageProducts",
  components: { SaleDialog, AlertSuccess, AlertError },
  data: () => ({
    saleItem: null,
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
    startSaleDialog(product_id) {
      this.saleItem = product_id;
    },
    stopSaleDialog() {
      this.saleItem = null;
    },
    showError(error_text) {
      this.failedOperation = error_text;
    },
    clearError() {
      this.failedOperation = null;
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
    registerSale(product_id, amount) {
      this.startSalePending();
      http_proxy()
        .post(`/products/${product_id}/sale`, { amount })
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
            this.showError(FAILED_SALE_NOT_AVAILABLE_PRODUCT);
          }
        })
        .finally(() => {
          setTimeout(() => {
            {
              this.stopSaleDialog();
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
