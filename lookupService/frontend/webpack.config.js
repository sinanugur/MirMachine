const path = require('path');

module.exports = {
    entry: './src/index.js',
    mode: 'development',
    output: {
        publicPath: '',
        filename: '[name].js',
        path: path.resolve(__dirname, '../static/frontend'),
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"],
            },
            {
                test: /\.(css|scss)$/,
                exclude: /node_modules/,
                use: ["style-loader", "css-loader"],
            },
            {
                test: /\.(less)$/,
                exclude: /node_modules/,
                use: ["style-loader", "css-loader", "less-loader"],
            },
            {
                test: /\.(jpg|jpeg|png|gif|mp3|svg)$/,
                exclude: /node_modules/,
                use: ["file-loader"],
            }
        ]
    },
};