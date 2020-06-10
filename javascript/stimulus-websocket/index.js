import StimulusReflex from "stimulus_reflex"
import ReconnectingWebSocket from "reconnecting-websocket"
import CableReady from "cable_ready"

const extend = function(object, properties) {
    if (properties != null) {
      for (let key in properties) {
        const value = properties[key]
        object[key] = value
      }
    }
    return object
}

class Subscription {
    constructor(consumer, params = {}, mixin) {
        this.consumer = consumer
        this.identifier = JSON.stringify(params)
        extend(this, mixin)
    }

    send(data) {
        return this.consumer.send(data)
      }

    unsubscribe() {
        return this.consumer.subscriptions.remove(this)
    }
}

class Subscriptions {
    constructor(consumer) {
        this.consumer = consumer
        this.subscriptions = []
    }

    findAll(identifier) {
        return this.subscriptions.filter((s) => s.identifier === identifier)
    }

    add(subscription) {
        this.subscriptions.push(subscription)
        // below functionality is not implemented
        // this.consumer.ensureActiveConnection()
        // this.notify(subscription, "initialized")

        // TODO we needo a subscribe command
        // this.sendCommand(subscription, "subscribe")
        return subscription
    }

    create(channelName, mixin) {
        const channel = channelName
        const params = typeof channel === "object" ? channel : {channel}
        const subscription = new Subscription(this.consumer, params, mixin)
        return this.add(subscription)
    }
}


class Consumer {
  constructor(url, options) {
    this.connection = new ReconnectingWebSocket(url, [], options || {})
    this.subscriptions = new Subscriptions(this)
  }

  send(data) {
    this.connection.send(data)
  }
}

const getConsumer = (url) => {
  // read up on the default options that actioncable has for websockets.
  let options = {
    maxRetries: 3,
    debug: true
  }

  return new Consumer(url, options)
}

const AbstractConsumerAdapter = StimulusReflex.getAbstractClass()

class WebsocketConsumer extends AbstractConsumerAdapter{
  constructor(consumer) {
    super(consumer)

    this.consumer.connection.addEventListener("message", (event) => {
      let data = JSON.parse(event.data)
      if (!data.cableReady) return
      if (!data.operations.morph || !data.operations.morph.length) return

      const urls = Array.from(
        new Set(data.operations.morph.map(m => m.stimulusReflex.url))
      )

      if (urls.length !== 1 || urls[0] !== (location.href)) return
      CableReady.perform(data.operations)
    })

    this.consumer.connection.addEventListener("message", (event) => {
      let data = JSON.parse(event.data)
      if (data.meta_type !== "cookie") return
      document.cookie = `${data.key}=${data.value||""}; max-age=${data.max_age}; path=/`
    })
  }

  find_subscription(identifier) {
    return this.consumer.subscriptions.findAll(identifier)[0]
  }

  create_subscription(channel) {
    this.consumer.subscriptions.create(channel)
  }

  connect() {
    return this.consumer.connection.open()
  }

  disconnect() {
    return this.consumer.connection.close()
  }

  isConnected() {
    return this.consumer.connection.readyState == ReconnectingWebSocket.OPEN
  }

  send(identifier, data, options) {
    let subscription = this.find_subscription(identifier)
    subscription.send(JSON.stringify(data))
    // return this.consumer.connection.send(JSON.stringify(data))
  }

}

export {
  WebsocketConsumer,
  getConsumer
}
