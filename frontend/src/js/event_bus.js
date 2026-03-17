(function () {
  const listeners = {};

  function subscribe(topic, fn) {
    if (!listeners[topic]) listeners[topic] = [];
    listeners[topic].push(fn);
  }

  function publish(topic, data) {
    (listeners[topic] || []).forEach(fn => fn(data));
  }

  window.EventBus = { subscribe, publish };
})();
