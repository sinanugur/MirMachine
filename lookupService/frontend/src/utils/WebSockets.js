import { baseURL } from '../config'

const wsURL = 'ws://' + baseURL + '/ws'

export const connectToSocket = (species, statusHook, progressHook, queueHook, initiationHook, completedHook) => {
    const socket = new WebSocket(wsURL + `/job/${species}`)
    // On open connection
    socket.addEventListener('open', (event) => {
        socket.send('request status')
        console.log('connected to socket')
    })
    // Listen for messages
    socket.addEventListener('message', (event) => {
        console.log('Message from server', event.data)
        let parsed = JSON.parse(event.data)
        if(parsed.type === 'status') {
            statusHook(parsed.status)
            if(parsed.status === 'ongoing') progressHook('0%')
        } else if(parsed.type === 'progress') {
            let progress = parsed.progress.split('(')[1].split(')')[0]
            progressHook(progress)
        } else if(parsed.type === 'queue'){
            queueHook(parsed.queuePos)
        } else if(parsed.type === 'initiation'){
            initiationHook(parsed.time)
        } else if(parsed.type === 'completed'){
            completedHook(parsed.time)
            progressHook('100%')
        } else if(parsed.type === 'model_change'){
            alert('Families included in your search and the model selected, were inconsistent.\n' +
                'We changed the model type to combined for you')
        }
    })

    // Listen for errors
    socket.addEventListener('error', (event) => {
        console.log('Error that occured: ', event)
    })

    // Listen for close
    socket.addEventListener('close', (event) => {
        console.log('Connection closed: ', event)
    })
    return socket
}
