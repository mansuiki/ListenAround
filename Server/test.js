const io = require('socket.io-client');

const socket = io("http://localhost:33333");

socket.on('get_a', (socket) => {
    console.log(socket)
});

socket.emit('put_a', {hi: 'hi'});