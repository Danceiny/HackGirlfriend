# -*- coding: utf-8
GET_ACCESS_TOKEN_BASE_URL = 'https://openapi.baidu.com/oauth/2.0/token'
APP_ID = '9670549'
API_KEY = '1IL7qqh6mB0CQG2u0e3h9U6U'
SECRET_KEY = 'adaa1876be9713c924b8003cda16bdec'

GET_ACCESS_TOKEN = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=1IL7qqh6mB0CQG2u0e3h9U6U&client_secret=adaa1876be9713c924b8003cda16bdec'
# params
GRANT_TYPE = 'client_credentials'

#  grant_type：必须参数，固定为 “client_credentials”；
#  client_id：必须参数，应用的 API Key；
#  client_secret：必须参数，应用的 Secret Key；


# expire: 1 month
GET_ACCESS_TOKEN_RESPONSE = {"access_token": "24.f0e768726fac1aa4708097b9e235f322.2592000.1498458389.282335-9670549",
                             "session_key": "9mzdXUSUxTGXKs2sL8xaKHLl4hBDql1njG8B8rbh82ubQ8tl2C785nhBeEpnHD8tjpvqEwHvZ7BJIdU8Qjq3J7o4Ztv6",
                             "scope": "public audio_voice_assistant_get audio_tts_post wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian wangrantest_test wangrantest_test1 bnstest_test1 bnstest_test2 vis-classify_flower",
                             "refresh_token": "25.eaebbc246dc1fd2777af28ec57c5deac.315360000.1811226389.282335-9670549",
                             "session_secret": "cbb091aaf6ce7ee9d007966c690e0f06", "expires_in": 2592000}

ACCESS_TOKEN = GET_ACCESS_TOKEN_RESPONSE['access_token']

API_BASE_URL = 'http://tsn.baidu.com/text2audio'
# params
TEXT = ''
