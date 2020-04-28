import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
import WebsocketConsumer from '../../../sockpuppet/static/js/reflex-websocket'
import ExampleController from './controllers/example_controller'

const application = Application.start()
const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("example", ExampleController)
StimulusReflex.initialize(application, { consumer })
