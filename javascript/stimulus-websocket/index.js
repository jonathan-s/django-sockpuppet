import ReconnectingWebSocket from "reconnecting-websocket"

// read up on the default options that actioncable has for websockets.

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
        return this.consumer.send(data, this.identifier)
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
        this.consumer.connection.send(JSON.stringify({
            type: 'subscribe',
            channelName: subscription.identifier
        }))
        return subscription
    }

    create(channelName, mixin) {
        const channel = channelName
        const params = typeof channel === "object" ? channel : {channel}
        const subscription = new Subscription(this.consumer, params, mixin)
        return this.add(subscription)
    }

    forget(subscription) {
      this.subscriptions = (this.subscriptions.filter((s) => s !== subscription))
      return subscription
    }

    remove(subscription) {
      this.forget(subscription)
      if (this.findAll(subscription.identifier).length == 0) {
        this.consumer.connection.send(JSON.stringify({
            type: 'unsubscribe',
            channelName: subscription.identifier
        }))
      }
      return subscription
    }

    notify(subscription, callbackName, ...args) {
      let subscriptions
      if (typeof subscription === "string") {
        subscriptions = this.findAll(subscription)
      } else {
        subscriptions = [subscription]
      }

      return subscriptions.map((subscription) =>
        (typeof subscription[callbackName] === "function" ? subscription[callbackName](...args) : undefined))
    }

    notifyAll(callbackName, ...args) {
      return this.subscriptions.map((subscription) =>
        this.notify(subscription, callbackName, ...args))
    }
}

export default class WebsocketConsumer {
    constructor(url, options = {}) {
        this._url = url
        this.subscriptions = new Subscriptions(this)

        options = {maxRetries: 3, ...options}
        this.connection = new ReconnectingWebSocket(url, [], options)
        this.connection.isOpen = function open() {
            return this.readyState === ReconnectingWebSocket.OPEN;
        }

        this.connection.addEventListener('open', (event) => {
          this.subscriptions.notifyAll('connected')
        })

        this.connection.addEventListener("message", (event) => {
            let data = JSON.parse(event.data)
            if (data.meta_type === 'cookie') {
              document.cookie = `${data.key}=${data.value||""}; max-age=${data.max_age}; path=/`;
              return
            }
            this.subscriptions.notify(data.identifier, 'received', data)
        })
    }

    get url() {
        return createWebSocketURL(this._url)
    }

    send(data, identifier) {
        data.identifier = identifier
        return this.connection.send(JSON.stringify(data))
    }

    connect() {
        return this.connection.open()
    }

    disconnect() {
        return this.connection.close()
    }
}
