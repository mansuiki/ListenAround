const http = require('http');

const httpServer = http.createServer((request, response) => {
    console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});
httpServer.listen(33333, () => {
    console.log((new Date()) + ' Server is listening on port 33333');
});

const io = require('socket.io')(httpServer);

io.on('connection', socket => {
    console.log(`[${new Date()}] Socket connected.`);
    var prevRoll = 0;
    var steps = 0;

    socket.emit('navigate', 1);

    socket.on('putq', msg => {
        const [roll, pitch, yaw] = msg;

        io.emit('getq', { roll, pitch, yaw });

        if ((85 < prevRoll && prevRoll < 100) && roll > 100) {
            console.log('walk', ++steps);
            io.emit('walk', 70);
        }

        prevRoll = roll;
    });

    socket.on('puto', msg => {
        try {
            const data = JSON.parse(msg);
            const result = data.map(
                o => {
                    const k = 0.02645833 * o.px;
                    const r =   Math.sqrt(Math.abs(o.dist*100 - k^2 - 0.09));
                    return {
                        type: o.type,
                        vx: k*r/0.03,
                        vy: r
                    };
                }

            );
            console.log(result);
            io.emit('geto', result);
        } catch (error) {
            console.error(error);
            io.emit('error', error);
        }
    });

    socket.on('putttt', msg => {
        console.log(msg);
        const val = Number(msg);
        io.emit('getttt',  Number(msg) /*0: 오른쪽, 1: 앞, 2: 왼쪽, 3: 뒤*/);
    });
});