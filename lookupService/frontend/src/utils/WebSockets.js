
export const connectToSocket = (id, statusHook, progressHook, queueHook) => {
    const socket = new WebSocket(`ws://localhost:8000/ws/job/${id}`)
    // On open connection
    socket.addEventListener('open', (event) => {
        socket.send('Current status please')
        console.log('connected to socket')
    })
    // Listen for messages
    socket.addEventListener('message', (event) => {
        console.log('Message from server', event.data)
        let parsed = JSON.parse(event.data)
        if(parsed.type === 'status'){
            statusHook(parsed.status)
            let progress = parsed.progress
            if(progress !== ''){
                let cleanedProgress = progress.split('(')[1].split(')')[0]
                progressHook(cleanedProgress)
            }
        } else if(parsed.type === 'queue'){
            queueHook(parsed.queuePos)
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
