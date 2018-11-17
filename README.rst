Home Assistant Addons
=====================

Couple of Home Assistant Addons

SMSApi notification component
-----------------------------

Component allowing to send SMS notifications using SMSApi.pl service.

Copy components/notify/smsapi.py to your custom_components/notify/ folder

Use following configuration in your configuration.yaml

.. code:: yaml

  notify:
  - name: smsapi_me
    platform: smsapi
    access_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    recipient: "+48666777888"

Get your access token from SMSApi.pl website. Go to `API settings <https://ssl.smsapi.pl/webapp#/oauth/manage>`__ and set up OAuth token.

Recipient is a mobile number with country prefix (+48 = Poland in this case).


Blebox wLightBoxS component
-----------------------------

.. code:: yaml

  light:
  - name: My Blebox Light
    platform: wlightboxs
    host: 192.168.0.100
