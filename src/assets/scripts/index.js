window.$ = window.jQuery = require('jquery')

require('bootstrap')
require('admin-lte')

import { initCoupons, initTooltip } from "./coupons";
import { initDashboard } from "./dashboard";

window.CouponScraper = (() => {
    initCoupons()

    if (window.location.pathname.indexOf('/tasks/') == 0) {
        initDashboard()
    }
    return {
        coupons: {
            init: initCoupons
        }
    }
})()