from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token") #通过url找到token
        # token = request.META.get("HTTP_Authorization") #通过请求头找到token
        if not token:
            raise AuthenticationFailed({"status":False,"message":"认证失败,请重新登录"})
        return "认证成功",token
    def authenticate_header(self, request): #确保返回异常状态的正确性
        return 'token'
