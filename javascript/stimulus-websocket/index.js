import ReconnectingWebSocket from "reconnecting-websocket"
import CableReady from "cable_ready"

// read up on the default options that actioncable has for websockets.

const options = {
    maxRetries: 3,
    debug: true
}

function createWebSocketURL(url) {
    if (typeof url === "function") {
      url = url()
    }

    if (url && !/^wss?:/i.test(url)) {
      const a = document.createElement("a")
      a.href = url
      // Fix populating Location properties in IE. Otherwise, protocol will be blank.
      a.href = a.href
      a.protocol = a.protocol.replace("http", "ws")
      return a.href
    } else {
      return url
    }
}

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

export default class WebsocketConsumer {
    constructor(url) {
        this._url = url
        this.subscriptions = new Subscriptions(this)

        this.connection = new ReconnectingWebSocket(url, [], options)
        this.connection.isOpen = function open() {
            return this.readyState === ReconnectingWebSocket.OPEN;
        }

        this.connection.addEventListener("message", (event) => {
            let data = JSON.parse(event.data)
            if (!data.cableReady) return
            if (!data.operations.morph || !data.operations.morph.length) return
            const urls = Array.from(
                new Set(data.operations.morph.map(m => m.stimulusReflex.url))
            )
            if (urls.length !== 1 || urls[0] !== (location.href)) return
            CableReady.perform(data.operations)
        })

        this.connection.addEventListener("message", (event) => {
            let data = JSON.parse(event.data)
            if (data.meta_type !== 'cookie') return
            document.cookie = `${data.key}=${data.value||""}; max-age=${data.max_age}; path=/`;
        })
    }

    get url() {
        return createWebSocketURL(this._url)
    }

    send(data) {
        return this.connection.send(JSON.stringify(data))
    }

    connect() {
        return this.connection.open()
    }

    disconnect() {
        return this.connection.close()
    }
}
