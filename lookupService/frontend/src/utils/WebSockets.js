
export const connectToSocket = (id, hook) => {
    const socket = new WebSocket(`ws://localhost:8000/ws/job/${id}`)
    // Open connection
    console.log('inside the connection method')
    socket.addEventListener('open', (event) => {
        socket.send('Nice to meet you')
        console.log('connected to socket')
    })
    // Listen for messages
    socket.addEventListener('message', (event) => {
        console.log('Message from server', event.data)
        hook(JSON.parse(event.data).status)
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
