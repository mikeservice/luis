export const getFeed = (callback) => {
    let $feedContainer = $("table#tasks-table tbody")
    $.ajax({
        url: "/tasks/feed",
        method: "post",
        success: (res) => {
            if (typeof callback === 'function') {
                callback(res)
            } else {
                $feedContainer.html(res)
            }
        }
    })
}

export default { getFeed }