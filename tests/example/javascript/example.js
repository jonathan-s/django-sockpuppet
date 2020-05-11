import { Application } from "stimulus"
import StimulusReflex from "stimulus_reflex"
// because travis had issues with 'sockpuppet-js' we had to do this.
import { WebsocketConsumer, getConsumer } from "../../../javascript/stimulus-websocket/index"
import ExampleController from "./controllers/example_controller"

const application = Application.start()
const realConsumer = getConsumer("ws://localhost:8000/ws/sockpuppet-sync")
const consumer = new WebsocketConsumer(realConsumer)

application.register("example", ExampleController)
StimulusReflex.initialize(application, { consumer })
