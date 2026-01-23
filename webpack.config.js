/**
 * Webpack configuration for bundling extension with dependencies
 * This bundles axios and dotenv into the extension to avoid runtime errors
 */

//@ts-check
'use strict';

const path = require('path');

/**@type {import('webpack').Configuration}*/
const config = {
    target: 'node', // VS Code extensions run in a Node.js context
    mode: 'none', // Leave source code as close as possible for debugging

    entry: './vscode-extension/src/extension.ts', // Entry point
    output: {
        path: path.resolve(__dirname, 'out'),
        filename: 'extension.js',
        libraryTarget: 'commonjs2',
        devtoolModuleFilenameTemplate: '../[resource-path]'
    },
    devtool: 'source-map',
    externals: {
        vscode: 'commonjs vscode' // VS Code API should not be bundled
    },
    resolve: {
        extensions: ['.ts', '.js']
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'ts-loader'
                    }
                ]
            }
        ]
    }
};

module.exports = config;
