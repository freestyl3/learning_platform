console.log('hello world quiz')

const url = window.location.href

$.ajax({
    type: 'GET',
    url: `${url}take_test`,
    success: function(response){
        console.log(response)
    },
    error: function(error){
        console.log(error)
    }
})