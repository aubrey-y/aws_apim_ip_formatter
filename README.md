# aws_apim_ip_formatter
Local script that automates the process of finding IP addresses for AWS `API_GATEWAY` service, and formatting them in
an acceptable format for Google Cloud's Admin API.

## Background
AWS (supposedly) regularly publishes IP addresses for all of its services at https://ip-ranges.amazonaws.com/ip-ranges.json

In order to batch whitelist these IP addresses (and blacklist everything else) to limit incoming traffic into the
base REST api, whose gateway is protected by API keys for a reason, this is a simple fix that does need to be run manually via
Google's Admin API [try it now](https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1beta/apps.firewall.ingressRules/batchUpdate?apix=true)
dialog.

## Future Improvements
Google Cloud's Admin API presents a lot of challenges, technically. In order to use it, a static
API Key and a dynamic header Bearer token are both required to authenticate. Anything less produces this error:

```json
{
  "error": {
    "code": 401,
    "message": "Request is missing required authentication credential. Expected OAuth 2 access token, login cookie or other valid authentication credential. See https://developers.google.com/identity/sign-in/web/devconsole-project.",
    "status": "UNAUTHENTICATED"
  }
}
```

So essentially, in order to get the bearer token, an initial request has to be sent to Google Cloud with a return
address, which must be available to receive a request from Google Cloud with a timeboxed Bearer token, valid for
something like 60 minutes.

That means an entirely separate/new service should probably be created to handle this process to finally `POST` to

`https://appengine.googleapis.com/v1beta/apps/<project_id>/firewall/ingressRules:batchUpdate?key=<api-key>`

Although this does raise the question about whether the API itself could handle that and whether Google Cloud
automatically whitelists requests from Google Cloud services.

Obviously, the implementation of something like that would take days at least, while this script took 5-10 minutes.
