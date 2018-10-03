export const initTooltip = () => {
    $("body").tooltip({
        selector: '[data-toggle="tooltip"]',
        container: 'body'
    });
}

export const initCoupons = () => {
    initTooltip()
}