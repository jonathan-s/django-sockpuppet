import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
import CableReady from 'cable_ready'
// because travis had issues with 'sockpuppet-js' we had to do this.
import WebsocketConsumer from '../../../javascript/stimulus-websocket/index'
import ExampleController from './controllers/example_controller'

const application = Application.start()
const consumer = new WebsocketConsumer(
  `ws://${window.location.host}/ws/sockpuppet-sync`, {debug: false}
)

consumer.subscriptions.create('progress', {
  received (data) {
    if (data.cableReady) CableReady.perform(data.operations)
  }
})
application.register("example", ExampleController)
StimulusReflex.initialize(application, { consumer, debug: true})
