# Design Document

## Component structure

```plantuml
top to bottom direction
skinparam linetype ortho

package apps {
[river-api]
[river-worker]
[river-web]
}
package packages {
[river-databases]
[river-connectors]
}

[river-core]

[river-web] -> [river-api]
[river-api] -> [river-worker]
[river-api] -> [river-databases]
[river-worker] --> [river-connectors]
[river-worker] --> [river-databases]
[river-databases] --> [river-core]
[river-connectors] --> [river-core]
```
