import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
// because travis had issues with 'sockpuppet-js' we had to do this.
import WebsocketConsumer from '../../javascript/stimulus-websocket/index'

const application = Application.start()
const consumer = new WebsocketConsumer(
  `${location.protocol=='https:'?'wss':'ws'}://${window.location.host}/ws/sockpuppet-sync`, {debug: false}
)

StimulusReflex.initialize(application, { consumer })
