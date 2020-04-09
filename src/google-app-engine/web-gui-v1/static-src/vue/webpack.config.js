var path = require('path')
var webpack = require('webpack')

/*** Loginform */

console.log(process.env.NODE_ENV);

if (process.env.NODE_ENV === 'development-login' || process.env.NODE_ENV === 'production-login') {
  var output = {
    path: path.resolve(__dirname, '../../static/javascript/'),
    publicPath: '../../static/javascript/',
    filename: 'me-loginform.js'
  };

  if (process.env.NODE_ENV === 'development-login') {
    output = {
      path: path.resolve(__dirname, './dist'),
      publicPath: '/dist/',
      filename: 'me-loginform.js'
    };
  }

  module.exports = {
    entry: './src/me-loginform.js',
    output: output,
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            'vue-style-loader',
            'css-loader'
          ],
        },      {
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {
            loaders: {
            }
            // other vue-loader options go here
          }
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          exclude: /node_modules/
        },
        {
          test: /\.(png|jpg|gif|svg)$/,
          loader: 'file-loader',
          options: {
            name: '[name].[ext]?[hash]'
          }
        }
      ]
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      },
      extensions: ['*', '.js', '.vue', '.json']
    },
    devServer: {
      historyApiFallback: true,
      noInfo: true,
      overlay: true
    },
    performance: {
      hints: false
    },
    devtool: '#eval-source-map'
  }
}

if (process.env.NODE_ENV === 'production-login') {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: false,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}

/*** Me-dashboard form */

if (process.env.NODE_ENV === 'development-dashboard' || process.env.NODE_ENV === 'production-dashboard') {
  var output = {
    path: path.resolve(__dirname, '../../static/javascript/'),
    publicPath: '../../static/javascript/',
    filename: 'me-dashboard.js'
  };

  if (process.env.NODE_ENV === 'development-dashboard') {
    output = {
      path: path.resolve(__dirname, './dist'),
      publicPath: '/dist/',
      filename: 'me-dashboard.js'
    };
  }

  module.exports = {
    entry: './src/me-dashboard.js',
    output: output,
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            'vue-style-loader',
            'css-loader'
          ],
        },      {
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {
            loaders: {
            }
            // other vue-loader options go here
          }
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          exclude: /node_modules/
        },
        {
          test: /\.(png|jpg|gif|svg)$/,
          loader: 'file-loader',
          options: {
            name: '[name].[ext]?[hash]'
          }
        }
      ]
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      },
      extensions: ['*', '.js', '.vue', '.json']
    },
    devServer: {
      historyApiFallback: true,
      noInfo: true,
      overlay: true
    },
    performance: {
      hints: false
    },
    devtool: '#eval-source-map'
  }
}

if (process.env.NODE_ENV === 'production-dashboard') {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: false,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
