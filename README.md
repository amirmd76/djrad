# Django-JSONRPC-REST-API-Decorators (DJRAD)

## Examples:

### New Rest API

```
@rest_api(method="POST", params=(("token", "std"), ("username", "true"), ("photo", "file", true)))
```

ALL FILES MUST HAVE TYPE IN ORDER FOR THIS TO WORK