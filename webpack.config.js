const webpack = require('webpack');
const glob = require('glob');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;


let globOptions = {
    ignore: ['node_modules/**', 'venv/**']
}

let entryFiles = glob.sync("**/javascript/*.js", globOptions)

let entryObj = {};
entryFiles.forEach(function(file){
    if (file.includes('.')) {
        let parts = file.split('/')
        let path = parts.pop()
        let fileName = path.split('.')[0];
        entryObj[fileName] = `./${file}`;
    }
});

let sockpuppet = {sockpuppet: "./sockpuppet/js/sockpuppet.js"}

module.exports = [
  function(env, argv) {
    isProd = process.env.NODE_ENV === 'production'
    let config = {
      mode: process.env.NODE_ENV,
      entry: entryObj,
      output: {
        path: __dirname + '/jsdist/js',
        filename: '[name].js'
      },
      optimization: {
        minimize: isProd
      },
      plugins: []
    }

    // if (env.analyze) {
    //   config.plugins.push(new BundleAnalyzerPlugin())
    // }
    return config
  },
  function(env, argv) {
    isProd = process.env.NODE_ENV === 'production'
    let config = {
      mode: process.env.NODE_ENV,
      entry: sockpuppet,
      output: {
        path: __dirname + '/sockpuppet/static/sockpuppet',
        filename: '[name].js'
      },
      optimization: {
        minimize: isProd
      },
      devtool: 'source-map',
      plugins: []
    }
    return config
  }
]
