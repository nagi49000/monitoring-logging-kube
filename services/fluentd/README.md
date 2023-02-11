# Fluentd

The basic fluentd image is missing a few plugins, which can be installed in a small dockerfile.

```
# in services/fluentd
docker build . -t fluentd:edge
```
