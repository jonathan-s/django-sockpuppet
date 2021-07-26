import { Application } from 'stimulus'
import { Sockpuppet } from 'sockpuppet-js'
import WebsocketConsumer from 'sockpuppet-js'
import {{ class_name }}Controller from './controllers/{{ reflex_name }}_controller'

const application = Application.start()
const consumer = new WebsocketConsumer(`ws://${window.location.host}/ws/sockpuppet-sync`)

application.register("{{ reflex_name }}", {{ class_name }}Controller)
Sockpuppet.initialize(application, { consumer })
