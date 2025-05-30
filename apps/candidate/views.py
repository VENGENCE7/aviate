
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models.functions import Length
from django.db.models import Q, Case, When, Value, IntegerField, ExpressionWrapper

from .models import Candidate
from .serializers import CandidateSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = None  # Disables pagination for this ViewSet

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        search_query = request.query_params.get('query', None)
        action_message = "Successfully retrieved the list of all candidates."

        if search_query and search_query.strip():
            # --- Search Logic ---
            action_message = f"Search results for query: '{search_query}'"
            search_words = sorted(
                list(set(word.lower() for word in search_query.split() if word.strip())))

            if not search_words:
                return Response(
                    {"error": "Search query parameter 'query' provided but contained no valid words after processing."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Apply search filters to the base queryset
            filter_conditions = Q()
            for word in search_words:
                filter_conditions |= Q(name__icontains=word)
            queryset = queryset.filter(filter_conditions)

            # Apply relevance annotation and ordering for search results
            print(search_words)
            relevance_score_annotation = ExpressionWrapper(
                Value(0), output_field=IntegerField())
            for word in search_words:
                relevance_score_annotation += Case(
                    When(name__icontains=word, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            queryset = queryset.annotate(
                relevance_score=relevance_score_annotation)
            queryset = queryset.order_by(
                '-relevance_score', Length('name'), 'name')

        serializer = self.get_serializer(queryset, many=True)

        custom_response_data = {
            'message': action_message,
            'status_code': status.HTTP_200_OK,
            'count': len(serializer.data),
            'results': serializer.data
        }

        return Response(custom_response_data, status=status.HTTP_200_OK)

    def createk(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        custom_response_data = {
            "message": "Candidate created successfully!",
            "status_code": status.HTTP_201_CREATED,
            "candidate_id": serializer.data.get('id'),
            "candidate_details": serializer.data
        }
        return Response(custom_response_data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        custom_response_data = {
            "message": "Candidate details retrieved successfully.",
            "status_code": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        custom_response_data = {
            "message": f"Candidate {'partially ' if partial else ''}updated successfully!",
            "status_code": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        candidate_id = instance.id
        candidate_name = instance.name
        self.perform_destroy(instance)

        custom_response_data = {
            "message": f"Candidate '{candidate_name}' (ID: {candidate_id}) deleted successfully.",
            "status_code": status.HTTP_200_OK
        }
        return Response(custom_response_data, status=status.HTTP_200_OK)
