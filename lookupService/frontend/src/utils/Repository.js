const baseURL = 'http://localhost:8000/api/'

export const submitJob = async (data) => {
    const csrftoken = getCookie('csrftoken')
    const jsonString = JSON.stringify(data,null, '    ')
    console.log(jsonString)

    const response = await fetch(baseURL + 'jobs/',{
        method: 'POST',
        mode: 'same-origin',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'X-CSRFToken': csrftoken,
            'Accept-Encoding': 'gzip, deflate, br'
        },
        body: jsonString
        });
    return response.json()
}

export const fetchJob = async (id) => {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(baseURL + `job/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    return response.json()
}

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break;
            }
        }
    }
    return cookieValue;
}
