# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_regional.api.admin.permissions import IsAdminUser
from django_regional.schemas.responses.currency import CurrencyListResponse
from django_regional.services import currency_service

_TAGS = ["Regional Currencies"]


class CurrencyListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=_TAGS,
        summary="List all currencies",
        description="Returns the full list of currencies from django_regional, ordered by ISO 4217 code. "
        "Unpaginated — dataset is small and bounded.",
        responses={200: CurrencyListResponse},
    )
    def get(self, request: Request) -> Response:
        results = currency_service.list_all()
        items = [item.model_dump() for item in results]
        return Response({"count": len(items), "next": None, "previous": None, "results": items})
