# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_regional.api.admin.permissions import IsAdminUser
from django_regional.schemas.responses.language import LanguageListResponse
from django_regional.services import language_service

_TAGS = ["Regional Languages"]


class LanguageListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=_TAGS,
        summary="List all languages",
        description="Returns the full list of languages from django_regional, ordered by Polish name. "
        "Unpaginated — dataset is small and bounded.",
        responses={200: LanguageListResponse},
    )
    def get(self, request: Request) -> Response:
        results = language_service.list_all()
        items = [item.model_dump() for item in results]
        return Response({"count": len(items), "next": None, "previous": None, "results": items})
