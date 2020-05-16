---
description: How to prepare your app to use StimulusReflex
---

# Setup

{% hint style="warning" %}
StimulusReflex v3 has been released, and there are some big changes. **Rails 6+ and server-side session storage are now required.**

You can find additional information for supporting Rails 5.2+ below.
{% endhint %}

StimulusReflex relies on [Stimulus](https://stimulusjs.org/), an excellent library from the creators of Rails. You can easily install StimulusReflex to new and existing Rails projects.

```bash
rails new myproject --webpack=stimulus
cd myproject
bundle add stimulus_reflex
bundle exec rails stimulus_reflex:install
```

The terminal commands above will ensure that both Stimulus and StimulusReflex are installed. It creates common files and an example to get you started. It also handles some of the configuration outlined below, including enabling caching in your development environment.

And that's it! **You can start using StimulusReflex in your application.**

{% hint style="danger" %}
Starting with v2.2.2 of StimulusReflex, support for the Rails default session storage mechanism `cookie_store` has been _temporarily_ dropped. The `stimulus_reflex:install` script will now set your session storage to be `:cache_store` in your development environment if no value has been set.
{% endhint %}

{% page-ref page="quickstart.md" %}

## Manual Configuration

Some developers will need more control than a one-size-fits-all install task, so we're going to step through what's actually required to get up and running with StimulusReflex in your Rails 6+ project.

First, the easy stuff: let's make sure we have [Stimulus ](https://stimulusjs.org)installed as part of our project's Webpack configuration. We'll also install the StimulusReflex gem and client library before enabling caching in your development environment.

```ruby
bundle exec rails webpacker:install:stimulus
bundle add stimulus_reflex
yarn add stimulus_reflex
rails dev:cache
```

We need to modify our Stimulus configuration to import and initialize StimulusReflex, which will attempt to locate the existing ActionCable consumer. A new websocket connection is created if the consumer isn't found.

{% tabs %}
{% tab title="app/javascript/controllers/index.js" %}
```javascript
import { Application } from 'stimulus'
import { definitionsFromContext } from 'stimulus/webpack-helpers'
import StimulusReflex from 'stimulus_reflex'
import consumer from '../channels/consumer'

const application = Application.start()
const context = require.context('controllers', true, /_controller\.js$/)
application.load(definitionsFromContext(context))
StimulusReflex.initialize(application, { consumer })
```
{% endtab %}
{% endtabs %}

Cookie-based session management is not currently supported by StimulusReflex. We will set our session management to be managed by the cache store, which in Rails defaults to the memory store.

{% code title="config/environments/development.rb" %}
```ruby
Rails.application.configure do
  config.session_store :cache_store
  # ....
end
```
{% endcode %}

You should also add the `action_cable_meta_tag`helper to your application template so that ActionCable can access important configuration settings:

{% code title="app/views/layouts/application.html.erb" %}
```markup
  <head>
    <%= csrf_meta_tags %>
    <%= csp_meta_tag %>
    <%= action_cable_meta_tag %>
  </head>
```
{% endcode %}

### Authentication

{% hint style="info" %}
If you're just experimenting with StimulusReflex or trying to bootstrap a proof-of-concept application on your local workstation, you can actually skip this section until you're planning to deploy.
{% endhint %}

Out of the box, ActionCable doesn't give StimulusReflex the ability to distinguish between multiple concurrent users looking at the same page.

**If you deploy to a host with more than one person accessing your app, you'll find that you're sharing a session and seeing other people's updates**. That isn't what most developers have in mind!

When the time comes, it's easy to configure your application to support authenticating users by their Rails session or current\_user scope. Just check out the Authentication page and choose your own adventure.

{% page-ref page="authentication.md" %}

## Session Storage

We are strong believers in the Rails Doctrine and work very hard to prioritize convention over configuration. Unfortunately, there are some inherent limitations to the way cookies are communicated via websockets that make it difficult to use cookies for session storage in production. We've had to make the decision to _temporarily_ drop support for the Rails default cookie-based session store.

This puts us in the awkward position of forcing an infrastructure change for some users that has nuanced implications.

We decided to default to using the `:cache_store` for `config.session_store` \(and enabling caching\) in the development environment if no other option has been declared. If you set a different session store in an initializer, please make sure that we're not clobbering your preferred store with our good intentions. The Rails default cache store is `:memory_store` which will get the job done in development but is not suitable or appropriate for production.

You can learn more about session storage on the Deployment page.

{% page-ref page="deployment.md" %}

## Logging

StimulusReflex supports both client and server logging of Reflexes.

{% page-ref page="troubleshooting.md" %}

## Rails 5.2+ Support

When the Rails core team renamed the ActionCable JS npm package from `actioncable` to `@rails/actioncable` it made it very difficult to reliably import ActionCable. After evaluating our options, we made the difficult decision of updating to the new package name and freezing _official_ Rails 5.2 support on the 2.2.x branch of StimulusReflex.

```ruby
bundle add stimulus_reflex --version "~> 2.2.3"
yarn add stimulus_reflex@2.2.3
```

While we don't have the resources to maintain two distinct package versions, we're proud of 2.2.x and consider it stable. In the unfortunate case of a critical security issue, we will make every attempt to backport hotfixes.

{% hint style="info" %}
There's nothing about StimulusReflex 3+ that shouldn't work fine in a Rails 5.2 app if you're willing to do a bit of manual package dependency management.
{% endhint %}

