/**
 * 使用nodejs创建本地的http服务
 * */
var http = require('http');
var url = require('url');
var path = require('path');
var fs = require('fs');
var previewConfig = require('../config/index').preview;
var httpProxy = require('http-proxy');
var proxy = httpProxy.createProxyServer(); // See (†)

var requestType = {
    "css": "text/css",
    "js": "text/javascript",
    "html": "text/html"
};

var proxyConfig = {
    target: previewConfig.target,
    changeOrigin: true,
};

//
http.createServer(function (request, response) {
    var pathName = url.parse(request.url).pathname;
    var realName = path.join('.', pathName);
    var ext = path.extname(pathName);
    ext = ext ? ext.slice(1) : 'unknown';

    // 走转发走
    if (pathName.indexOf(previewConfig.prefix) !== -1) {

        previewConfig.debug && console.log(`Rewriting path from "${pathName}" =====> to "${proxyConfig.target}${pathName}"`);
        proxy.web(request, response, proxyConfig);
        return;
    }

    if (pathName.indexOf(previewConfig.staticDir) === -1) {
        pathName = '/index.html';
    }


    realName = path.join(__dirname, previewConfig.dir, pathName);

    previewConfig.debug && console.log(realName);

    fs.exists(realName, function (exists) {
        if (!exists) {
            response.writeHead(404, {'Context-type': 'text/plain'});
            response.write('this request url ' + pathName + ' was not found on this server.');
            response.end();
        } else {
            fs.readFile(realName, 'binary', function (err, file) {
                if (err) {
                    response.writeHead(500, {'Context-type': 'text/plain'});
                    response.end(err);
                } else {
                    var contentType = requestType[ext] || "text/plain";
                    response.writeHead(200, {'Context-type': contentType});
                    response.write(file, 'binary');
                    response.end();
                }
            });
        }
    });

}).listen(previewConfig.port, previewConfig.host);
console.log(`server running at http://${previewConfig.host}:${previewConfig.port}/`);
