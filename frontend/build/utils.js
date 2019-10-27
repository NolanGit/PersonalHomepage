'use strict'
const path = require('path')
const config = require('../config')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const packageConfig = require('../package.json');

const isProd = process.env.NODE_ENV === 'production';

//
exports.assetsPath = function (_path) {
    const assetsSubDirectory = isProd ? config.build.assetsSubDirectory : config.dev.assetsSubDirectory;

    //
    return path.join(assetsSubDirectory, _path);
};

//
exports.cssLoaders = function (options) {
    options = options || {}

    // css-loader
    const cssLoader = {
        loader: 'css-loader',
        options: {
            sourceMap: options.sourceMap
        }
    }

    // postcss
    const postcssLoader = {
        loader: 'postcss-loader',
        options: {
            sourceMap: options.sourceMap
        }
    }

    // generate loader string to be used with extract text plugin
    function generateLoaders(loader, loaderOptions) {
        //
        const loaders = []

        // Extract CSS when that option is specified
        // (which is the case during production build)
        if (options.extract) {
            loaders.push(MiniCssExtractPlugin.loader)
        } else {
            loaders.push('vue-style-loader')
        }

        loaders.push(cssLoader)

        if (options.usePostCSS) {
            loaders.push(postcssLoader)
        }

        if (loader) {
            loaders.push({
                loader: loader + '-loader',
                options: Object.assign({}, loaderOptions, {
                    sourceMap: options.sourceMap
                })
            })
        }

        return loaders
    }
    // https://vue-loader.vuejs.org/en/configurations/extract-css.html
    return {
        css: generateLoaders(),
        postcss: generateLoaders(),
        scss: generateLoaders('sass'),
    }

};

//
exports.styleLoaders = function (options) {
    const output = []
    const loaders = exports.cssLoaders(options)

    for (const extension in loaders) {
        const loader = loaders[extension]
        output.push({
            test: new RegExp('\\.' + extension + '$'),
            use: loader
        })
    }

    return output
};

