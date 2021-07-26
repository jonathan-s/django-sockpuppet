import { Controller } from 'stimulus'
import { Sockpuppet } from 'sockpuppet-js'

export default class extends Controller {
  connect() {
    Sockpuppet.register(this)
  }

  increment(event) {
    console.log('increment')
    event.preventDefault()
    this.stimulate('{{ class_name }}Reflex#increment', 1)
  }
}
