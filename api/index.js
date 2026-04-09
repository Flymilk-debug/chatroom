const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

// 在线用户列表
let users = [];

// 托管静态页面
app.use(express.static('public'));

// 处理连接
io.on('connection', (socket) => {
  console.log('用户连接:', socket.id);

  // 用户加入，设置昵称和标签
  socket.on('userJoin', (data) => {
    const { username, tags } = data;
    users = users.filter(u => u.id !== socket.id);
    users.push({
      id: socket.id,
      username,
      tags: tags.split(',').map(t => t.trim()).filter(t => t)
    });
    io.emit('userList', users);
  });

  // 处理聊天消息
  socket.on('chatMessage', (msg) => {
    io.emit('message', msg);
  });

  // 处理断开连接
  socket.on('disconnect', () => {
    users = users.filter(u => u.id !== socket.id);
    io.emit('userList', users);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
});

module.exports = app;
