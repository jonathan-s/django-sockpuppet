import babel from "rollup-plugin-babel"
import { terser } from "rollup-plugin-terser"
import resolve from "@rollup/plugin-node-resolve"
import commonjs from '@rollup/plugin-commonjs'

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
    input: "javascript/cable_ready/cable_ready.js",
    output: {
        file: "sockpuppet/static/js/cable_ready.js",
        format: "umd",
        name: "CableReady"
    },
    plugins: [
        // babel({
        //     exclude: "node_modules/**"
        // }),
        terser(options),
        resolve()
    ]
  },
  {
    input: "javascript/stimulus/stimulus_reflex.js",
    output: {
        file: "sockpuppet/static/js/stimulus_reflex.js",
        format: "umd",
        name: "StimulusReflex"
    },
    plugins: [
        resolve(),
        commonjs({
            namedExports: {
                "node_modules/@rails/actioncable/app/assets/javascripts/action_cable.js": ["createConsumer"]
            }
        }),
        babel(),
        terser(options),
    ]
  },
]
