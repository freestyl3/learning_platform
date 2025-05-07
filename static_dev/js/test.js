console.log('hello world quiz')

const url = window.location.href
const testBox = document.getElementById('test-box')
let data


$.ajax({
    type: 'GET',
    url: `${url}take_test`,
    success: function(response){
        data = response.data
        console.log(data)
        data.forEach(el => {
            for (const [question, data] of Object.entries(el)){
                testBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>   
                `
                if (data['type'] == 'choices' ){
                    data['answers'].forEach(answer => {
                        testBox.innerHTML += `
                            <div>
                                <input type="checkbox" class="choice-answer" id="${question}-${answer}" name="${question}" value="${answer}">
                                <label for="${question}">${answer}</label>
                            </div>
                        `
                    })
                } else if (data['type'] == 'input'){
                    testBox.innerHTML += `
                        <div>
                            <input type="text" class="input-answer" id="${question}-${data['answers'][0]}" name="${question}">
                        </div>
                    `
                } else if (data['type'] == 'matching') {
                    let html = `<ul>`
                    for (let i = 0; i < data['answers'].length; i++) {
                        html += `
                            <li>
                                ${data['answers'][i]} - <span draggable="true">${data['match_pairs'][i]}</span>
                            </li>
                        `
                    }
                    html += `</ul>`
                    testBox.innerHTML += html
                }
            }
        });
    },
    error: function(error){
        console.log(error)
    }
})