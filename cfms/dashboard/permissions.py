from django.core.exceptions import PermissionDenied

class AssignedAgentRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.assigned_agent_ref != request.user:
            raise PermissionDenied("Not your assigned complaint")

        return super().dispatch(request, *args, **kwargs)
    
class OwnComplaintRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.customer_account_ref != request.user:
            raise PermissionDenied("Not your complaint")

        return super().dispatch(request, *args, **kwargs)