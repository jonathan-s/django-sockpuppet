import { Controller } from 'stimulus';
import StimulusReflex from 'stimulus_reflex';

export default class extends Controller {
  connect() {
    StimulusReflex.register(this)
  }

  increment(event) {
    console.log('increment')
    event.preventDefault()
    this.stimulate('ExampleReflex#increment', 1)
  }
}
