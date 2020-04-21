import babel from "rollup-plugin-babel"
import { terser } from "rollup-plugin-terser"
import resolve from "@rollup/plugin-node-resolve"


const options = {
  mangle: false,
  compress: false,
  output: {
    beautify: true,
    indent_level: 2
  }
}

export default [
  {
    input: "javascript/stimulus-websocket/index.js",
    output: {
        file: "sockpuppet/static/js/reflex-websocket.js",
        format: "umd",
        name: "ReflexWebsocket"
    },
    plugins: [
        resolve(),
        babel(),
        terser(options),
    ]
  },
]
