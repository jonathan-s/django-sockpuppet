import { Controller } from 'stimulus'
import StimulusReflex from "stimulus_reflex"
import { reflexControllerMethods, received } from "stimulus_reflex/javascript/reflexes"
import actionCable from 'stimulus_reflex/javascript/transports/action_cable'
import Debug from 'stimulus_reflex/javascript/debug'
import Deprecate from 'stimulus_reflex/javascript/deprecate'
import { WebsocketConsumer } from './websocket'


let globalConsumer
let params
// read up on the default options that actioncable has for websockets.

class StimulusReflexController extends Controller {
  constructor (...args) {
    super(...args)
    register(this)
  }
}

const createSubscription = controller => {
  let consumer = globalConsumer || controller.application.consumer
  const { channel } = controller.StimulusReflex
  const subscription = { channel, ...params }
  const identifier = JSON.stringify(subscription)

  controller.StimulusReflex.subscription =
    consumer.subscriptions.findAll(identifier)[0] ||
    consumer.subscriptions.create(subscription, {
      received: received,
      connected: actionCable.connected,

      // these are currently never called.
      rejected: actionCable.rejected,
      disconnected: actionCable.disconnected
    })
}


const register = (controller, options = {}) => {
  const channel = 'StimulusReflex::Channel'
  controller.StimulusReflex = { ...options, channel }

  createSubscription(controller)
  Object.assign(controller, reflexControllerMethods)
}

const initialize = (application, {
  controller = StimulusReflexController,
  consumer,
  debug,
  params,
  isolate,
  deprecate
} = {}) => {
  let options = {consumer, controller, debug, params, isolate, deprecate}
  globalConsumer = consumer
  StimulusReflex.initialize(application, options)
}


const Sockpuppet = {
  initialize: initialize,
  register: register,
  get debug () {
    return Debug.value
  },
  set debug (value) {
    Debug.set(!!value)
  },
  get deprecate () {
    return Deprecate.value
  },
  set deprecate (value) {
    Deprecate.set(!!value)
  }
}

export {
  Sockpuppet
}

export default WebsocketConsumer
