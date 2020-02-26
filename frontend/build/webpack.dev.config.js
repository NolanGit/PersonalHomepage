const path = require('path')
const utils = require('./utils')
const webpack = require('webpack')

const config = require('../config');
//
const merge = require('webpack-merge');

const baseWebpackConfig = require('./webpack.base.config')

// html webpack plugin
const HtmlWebpackPlugin = require('html-webpack-plugin')

// friendly errors webpack plugin
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')

// port finder
const portfinder = require('portfinder')


const devWebpackConfig = merge(baseWebpackConfig, {
    mode: "development",
    output: {
        publicPath: config.dev.assetsPublicPath
    },
    module: {
        rules: utils.styleLoaders({
            sourceMap: config.dev.cssSourceMap,
        })
    },
    devtool: config.dev.devtool,
    devServer: {
        clientLogLevel: 'warning', //
        historyApiFallback: true, //
        hot: true, //
        compress: true, //
        host: config.dev.host,
        port: config.dev.port,
        open: config.dev.autoOpenBrowser,
        overlay: config.dev.errorOverlay
            ? {warnings: false, errors: true}
            : false,
        publicPath: config.dev.assetsPublicPath,
        proxy: config.dev.proxyTable,
        quiet: true, //
        watchOptions: {
            poll: config.dev.poll
        }
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': require('../config/dev.env')
        }),
        new webpack.HotModuleReplacementPlugin(),
        // https://github.com/ampedandwired/html-webpack-plugin
        new HtmlWebpackPlugin({
            template: 'src/index.html'
        })
    ]
});


module.exports = new Promise((resolve, reject) => {
    portfinder.basePort = process.env.PORT || config.dev.port;
    portfinder.getPort((err, port) => {
        if (err) {
            reject(err);
        } else {
            process.env.PORT = port;

            devWebpackConfig.devServer.port = port;

            devWebpackConfig.plugins.push(new FriendlyErrorsPlugin({
                compilationSuccessInfo: {
                    messages: [
                        `Your application is running here: http://${
                            devWebpackConfig.devServer.host
                            }:${port}`
                    ]
                }
            }));

            resolve(devWebpackConfig);
        }
    })
});
