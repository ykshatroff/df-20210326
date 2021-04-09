from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import connection, connections, DatabaseError

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from tg_react.api.accounts.serializers import SignupSerializer
from tg_react.api.accounts.views import SignUpView as TgReactSignUpView
from tg_react.api.accounts.views import UserDetails as TgReactUserDetails

from accounts.models import User
from accounts.rest.serializers import UserSerializer, UserCreateSerializer


class UserDetails(TgReactUserDetails):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES


class SignUpView(TgReactSignUpView):
    serializer_class = SignupSerializer

    def post(self, request):
        # TG_REACT_UPGRADE: Code is copied over to correctly create Organizations
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            data: dict = serializer.validated_data.copy()
            password = data.pop("password", None)

            user = get_user_model()(**data)
            user.set_password(password)
            user.save()

            serializer = TokenObtainPairSerializer(data={"email": user.email, "password": password})
            serializer.is_valid()
            # serializer = TokenObtainPairSerializer(data=request.data)
            return Response(serializer.validated_data)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DemoAdminUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_connection(self, user: User):
        db_user_name = f"user_{user.id}"
        db = settings.DATABASES["default"]

        new_database = {
            "id": db_user_name,
            "ENGINE": db["ENGINE"],
            "NAME": user.database,
            "USER": db_user_name,
            "PASSWORD": user.database_password,
            "HOST": db["HOST"],
            "PORT": db["PORT"],
        }

        connections.databases[db_user_name] = new_database
        return connections[db_user_name]

    def get(self, request):
        user = request.user
        conn = self.get_connection(user)
        cursor = conn.cursor()
        data = {"status": "ok", "data": []}
        try:
            cursor.execute("""SELECT * from users""")
        except DatabaseError:
            pass
        else:
            users = cursor.fetchall()
            columns = cursor.description
            users = [
                {c.name: f for c, f in zip(columns, u)}
                for u in users
            ]
            data["data"] = UserSerializer(users, many=True).data
        return Response(data)

    def post(self, request):
        user = request.user
        conn = self.get_connection(user)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL DEFAULT '',
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN NOT NULL DEFAULT false
        )""")

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cursor.execute("""INSERT INTO users (id, name, created_at, active, password) VALUES (
            DEFAULT,
            %(name)s,
            DEFAULT,
            %(active)s,
            %(password)s
        ) RETURNING *""", data)

        user_data = cursor.fetchone()
        columns = cursor.description
        user = {c.name: f for c, f in zip(columns, user_data)}

        return Response({"status": "ok", "data": UserSerializer(user).data}, status=201)
