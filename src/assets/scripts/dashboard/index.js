import API from "../common";

export const initDashboard = (callback) => {
    let dashboardTimer = window.setInterval(() => {
        API.dashboard.getFeed()
    }, 2000)
}