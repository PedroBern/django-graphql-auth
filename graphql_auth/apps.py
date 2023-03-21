from django.apps import AppConfig


class GraphQLAuthConfig(AppConfig):
    name = "graphql_auth"
    verbose_name = "GraphQL Auth"
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import graphql_auth.signals
