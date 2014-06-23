To use this file you will need the following:

1. IP address of your hue bridge.
2. You will need your phone’s authentication token for Philips hue. This can be found by doing a packet capture on your phone when the Hue app is clicked. Locate any conversation where your phone is the source and the bridge is the destination. These should be GET or POST requests and should read something like:

GET /api/**AUTHENTICATION TOKEN** HTTP/1.1

Once you have located the hueIP and the authentication please change these variables in the code
