import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
import WebsocketConsumer from 'sockpuppet-js'
import {{reflex_name|title }}Controller from './controllers/{{reflex_name}}_controller'

const application = Application.start()
const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("{{ reflex_name }}", {{ reflex_name|title }}Controller)
StimulusReflex.initialize(application, { consumer })
