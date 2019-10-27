const path = require('path')

const utils = require('./utils')

const config = require('../config')
// vue loader plugin
const {VueLoaderPlugin} = require('vue-loader');

//
function resolve(dir) {
    return path.join(__dirname, '..', dir);
}

module.exports = {
    //
    context: path.resolve(__dirname, '../'),
    //
    entry: {
        app: './src/main.js'
    },
    //
    output: {
        path: config.build.assetsRoot,
        filename: "[name].js"
    },
    //
    resolve: {
        extensions: ['.js', '.vue', '.json'],
        alias: {
            '~': resolve('src')
        }
    },
    //
    module: {
        rules: [
            // vue-loader
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            // js  cache directory
            {
                test: /\.js$/,
                loader: 'babel-loader?cacheDirectory',
                include: [
                    resolve('src'),
                    resolve('node_modules/webpack-dev-server/client')
                ]
            },
            // svg sprite loader
            {
                test: /\.svg$/,
                loader: 'svg-sprite-loader',
                include: [resolve('src/icons')],
                options: {
                    symbolId: 'icon-[name]'
                }
            },
            // img
            {
                test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
                loader: 'url-loader',
                exclude: [resolve('src/icons')],
                options: {
                    limit: 10000,
                    name: utils.assetsPath('img/[name].[hash:7].[ext]')
                }
            },
            // font
            {
                test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 100000,
                    name: utils.assetsPath('fonts/[name].[hash:7].[ext]')
                }
            }
        ]
    },
    plugins: [new VueLoaderPlugin()]
};
