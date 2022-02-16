import { JobFetchError, JobPostError, ResultFetchError } from './Errors'
import { validFile } from './Validators'
import { baseURL } from '../config'

const apiURL = 'http://' + baseURL + '/api/'

export const submitJob = async (data, file) => {
    const csrftoken = getCookie('csrftoken')
    const userAllowed = await checkIfUserCanPost(csrftoken)
    if(!userAllowed.message){
        throw new JobPostError('Please cancel ongoing or queued jobs before submitting a new one')
    }
    let formData = new FormData()
    const jsonString = JSON.stringify(data,null, '    ')
    formData.append('data', jsonString)

    if(data.mode == 'file'){
        if(!file) throw new JobPostError('Please select a file to upload')
        let isValidFile = await validFile(file)
        if(!isValidFile) throw new JobPostError('The selected file is invalid. \nLegal characters include "agtcun" excluding the header. ')
        formData.append('file', file)
    }



    const response = await fetch(apiURL + 'jobs/',{
        method: 'POST',
        mode: 'same-origin',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Accept': '*/*',
            'X-CSRFToken': csrftoken,
            'Accept-Encoding': 'gzip, deflate, br'
        },
        body: formData
        });
    if(response.status === 400){
        throw new JobPostError('Invalid data, make sure you filled out the necessary fields')
    } else if(response.status === 404){
        let message = await response.json()
        throw new JobPostError(message.message)
    } else if(response.status === 503){
        throw new JobPostError('The NCBI database returned an error')
    } else if(response.status === 403){
        let message = await response.json()
        if(message.message){
            throw new JobPostError(message.message)
        } else if(message.detail){
            throw new JobPostError('Please wait before submitting more jobs')
        }
    }
    return response.json()
}

export const fetchJob = async (id) => {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(apiURL + `job/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    switch (response.status) {
        case 200:
            return response.json()
            break
        case 400:
            throw new JobFetchError("String is not a valid ID")
            break
        case 404:
            throw new JobFetchError("Could not find the job in the database")
            break
        default:
            throw new JobFetchError("Unknown error occured")
            break
    }
}

export const cancelJob = async (_id) => {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(apiURL + 'jobs/?id=' + _id,{
        method: 'DELETE',
        mode: 'same-origin',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Accept': '*/*',
            'X-CSRFToken': csrftoken,
            'Accept-Encoding': 'gzip, deflate, br'
        }
    });
    if(response.status === 200) alert('Job successfully deleted')
    else alert('Something went wrong when aborting job')
}

export const getResults = async (_id) => {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(apiURL + `result/${_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    if(response.status === 200){
       return response.json()
    } else {
        let message = await response.json()
        throw new ResultFetchError(message.message)
    }
}


export const fetchTree = async () => {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(apiURL + `tree/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    return processTreeResponse(await response.json())
}

export const processTreeResponse = (response) => {
    let edges = []
    let nodes = []
    for(let i = 0; i<response.edges.length; i++){
        let cur = response.edges[i]
        edges.push({
            id: cur.id,
            from: cur.from_node,
            to: cur.to_node
        })
    }
    for(let i = 0; i<response.nodes.length; i++){
        let cur = response.nodes[i]
        let text = cur.text.startsWith("Artificial-node") ? "" : cur.text.replaceAll("_"," ")
        nodes.push({
            id: cur.id,
            text: text,
        })
    }
    return {nodes: nodes, edges: edges}
}

export const getFamilies = async () => {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(apiURL + `families/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    return response.json()
}

export const getFamiliesIncludedInSearch = async (node, bothWays, singleNode) => {
    const csrftoken = getCookie('csrftoken')
    const params = `?node=${node}&both_ways=${bothWays}&single_node=${singleNode}`
    const response = await fetch(apiURL + `relations/${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    return response.json()
}

export const checkIfNewUser = async () => {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(apiURL + 'cookiePrompt/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    return response.json()
}

const checkIfUserCanPost = async (cookie) => {
    const response = await fetch(apiURL + 'userCanPost/',{
        method: 'GET',
        headers: {
            'X-CSRFToken': cookie,
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
