$("#content").html($("#details").html())
$("#works_list").html($(".work_deck .all_works").html())

const details = () => {
    $("#content").html($("#details").html())
}

const clb = () =>  {
    $("#content").html($("#collaborators").html())
}

const works = () => {
    $("#content").html($("#works").html())
}

const ap = () => {
    $("#content").html($("#admin").html())
}

const leave = () => {
    $("#content").html($("#leave").html())
}

const all_work = () => {
    $("#works_list").html($(".work_deck .all_works").html())
}

const your_work = () => {
    $("#works_list").html($(".work_deck .your_works").html())
}

const add_work = () => {
    $("#content").html($("#add_work").html())
}

