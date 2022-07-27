module.exports = {
    "main view of application is loading": (browser) => {
        browser
            .init()
            .waitForElementVisible("#app", 2000)
            .assert.elementPresent(".manage-products")
            .assert.titleContains("Warehouse")
            .end();
    },
    "products are loaded": (browser) => {
        browser
            .init()
            .assert.textContains(".v-data-table", "Product 1")
            .assert.textContains(".v-data-table", "Product 2")
            .assert.textContains(".v-data-table", "Product 3").end();
    },
    "sale button triggers modal": (browser) => {
        browser
            .init()
            .click(".sale-button:first-of-type")
            .waitForElementVisible(".confirm-button", 1000)
            .assert.textContains(".v-dialog__content .v-toolbar__content", "Register sale #1111")
            .end();
    },
    "sale process": (browser) => {
        browser
            .init()
            .click(".sale-button:first-of-type")
            .waitForElementVisible(".confirm-button", 1000)
            .click(".confirm-button")
            .waitForElementVisible(".confirm-button", 1000)
            .assert.textContains('.v-alert__content', "Sale confirmed for Product: 1111")
            .end();
    },
};
