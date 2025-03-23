class CheckPermissionUseCase:
    def __init__(self, permission_service):
        self.permission_service = permission_service

    def execute(self, user, action, resource):
        return self.permission_service.check_permission(user, action, resource)
