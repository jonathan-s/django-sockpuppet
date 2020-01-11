import babel from "rollup-plugin-babel"
import uglify from "rollup-plugin-uglify"

const uglifyOptions = {
  mangle: false,
  compress: false,
  output: {
    beautify: true,
    indent_level: 2
  }
}

export default {
  input: "javascript/action_cable/index.js",
  output: {
    file: "sockpuppet/static/js/action_cable.js",
    format: "umd",
    name: "ActionCable"
  },
  plugins: [
    babel(),
    uglify(uglifyOptions)
  ]
}
