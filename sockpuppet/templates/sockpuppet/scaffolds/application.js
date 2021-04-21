import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
import WebsocketConsumer from 'sockpuppet-js'
import {{ class_name }}Controller from './controllers/{{ reflex_name }}_controller'

const application = Application.start()
const consumer = new WebsocketConsumer(`ws://${window.location.host}/ws/sockpuppet-sync`)

application.register("{{ reflex_name }}", {{ class_name }}Controller)
StimulusReflex.initialize(application, { consumer })
