import babel from "rollup-plugin-babel"
import uglify from "rollup-plugin-uglify"
import resolve from "rollup-plugin-node-resolve"

const uglifyOptions = {
  mangle: false,
  compress: false,
  output: {
    beautify: true,
    indent_level: 2
  }
}

export default [
  {
    input: "javascript/cable_ready/cable_ready.js",
    output: {
        file: "sockpuppet/static/js/cable_ready.js",
        format: "umd",
        name: "CableReady"
    },
    plugins: [
        babel(),
        uglify(uglifyOptions),
        resolve()
    ]
  }
]
