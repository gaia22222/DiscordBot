from datetime import datetime, timedelta
import os

def NowTime():
    return datetime.now() + timedelta(hours=8)

def GetGoogleAPI():
    return {
  "type": "service_account",
  "project_id": "gaia-394416",
  "private_key_id": os.environ.get('GOOGLE'),
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDB5a9Mo6uLGrmU\naKGI1VQlsbbSyj+w4a6p232NqdUIPuORy6mUYfqY43rP1gLKwfweAiy9LOXZ9Tg3\nI8EmVhLnq5XIEZBFgyd4ZZemES7PhcaBYHFtB2FDZcUu9ZbLpXRkm1TAoI4mhjZo\nxLi2xXyBKJX3VlHOY8tVXsQbPaqXHIxW8yM0ZHclN3pCZ5uifvgM4ayD1plvpxLS\nWXi5raJf88zTpIonK+Ziib34ZKqACNCeZdxrwHgrUDXgw9g7e9Y0TL6j70gYM9I1\nMZvB6vsrxHlqE5oBEjhr71O1Fh9BOGPIqF3V5yAa6h9mHa9wQoVBCMoqKvm7x0j0\nCXLTvMH7AgMBAAECggEAXMGbgD7F6BhDUhdRu0tOY2/mJWWiXWRBMbmyEOx/YF/x\nbsQunjDW+H/ONxHKqSNukA57R45scL2qBFrC4iuIBLLlRt38Ffzdi2+SQdvzeEwn\nP6oa6M0AfwT29PWAi3Bdw2k5fKLyDcTjz2/Ya3sDCiiXwUhWfzTnRzI7/0obSwkD\n0MVKxCsj4qFBVZ7u+6qgzZAL1q7GM4Lt+eMomEFCD0jAKDytPZKPUJvWP1tRtdyC\ndnz9kGT15LXPWZQHjDZ8Si/Gbn9NOe4DwsfstqAioHKuyobsZQYbUH+My+EKnXz9\nK4+6kFV8MGByzPJ5EoySqPgX2KnwIQlk6ZjzVSEelQKBgQDxfA1SH0FqGlNglzve\nEHWGQB/wYL7TSU7E7M74Q/dH/WfONCn/Grpumk1l6g59+tdLtca4BYNOL+23feZ8\nP6CeaUabm0DP4Cnzp2z+DEhHjw1h436pegGkvgoM+jO6f/cjSBtgTIAW/CmCe/bk\n3apXHuYwpjAoXahvgpBaEQNm7wKBgQDNjVyOAvtTUQgFP27v/dDzsMymHOgWrOcd\nUU/epjmBITqJSgph4FCFZ6c4EO/QpA6hKDw1dT8y7QUe9x9HN47VfdXN7lqnOcWR\nUXTPkD0oYcUpxANVWOF72f+biH4PcApJ8OeLZSOiLMu/zGX72NdD1jsbFEUE7Ljk\nPPMgVFK1tQKBgFA3Tw16iHZAbHXnhuGLQh7oajOlT35MGbhcmZvqp9foG3Vp6pFt\nRYS8CP3TtCCxFJd3uJ0kZ6uvTB3p2ohncmlsuyGxfuQOqKDhetkhJ1lt8ZoUwdx2\nRNl+r0QEUO6g122G5GEmyF3aQceweiEoaQ8rmneKnPCru+neyyjAAgtNAoGAZHQd\nM1nJsWH8ZXQmpyqHn1Bb8yJVWh+NowpF2i2qFK1Eiiug/0w8jbWmRwQf7vr+G0wq\ngIWYKS8kPYnPw2Inb7ZbcpR1wRu+rdH9ICMBgGankE22w1L4fyp+fGgsEydSH+iX\nf8whqfPybv1ZKcdDDGf54rX5NPrrML+IodgTw7ECgYEA12hqcI4qnftiYxrLBNUn\njpWeaQ3Vx2cXFmcYPphX9hu2OFmhHKeUd2zSQc8O0q5UiKFBrhHwMVjhY4KR0Rcg\nZHC3UGufHeYNcNPoU5aZ3AydaU0TqBK9JZuOT+3q5F/daod3tLoiMsyaj7/Awf1u\nWhATy+q9rlrN6DUjGl9Kulo=\n-----END PRIVATE KEY-----\n",
  "client_email": "gaia-770@gaia-394416.iam.gserviceaccount.com",
  "client_id": "102950876049806900435",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gaia-770%40gaia-394416.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

