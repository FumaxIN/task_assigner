# Utils/Views Quick Reference

> Django REST Framework utilities for dynamic serializers, permissions, and partial updates.

## Files

| File | Purpose |
|------|---------|
| `base.py` | Base viewset combining common mixins |
| `mixins.py` | Reusable mixins for DRF viewsets |
| `__init__.py` | Python package marker |

## Quick Start

```python
from utils.views.base import BaseModelViewSetPlain
from rest_framework.viewsets import ModelViewSet

class MyViewSet(BaseModelViewSetPlain, ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    
    # Action-specific serializers
    serializer_action_classes = {
        'create': CreateSerializer,
        'update': UpdateSerializer,
    }
    
    # Action-specific permissions
    permission_action_classes = {
        'create': [IsAdminUser()],
        'list': [IsAuthenticated()],
    }
```

## Components

### BaseModelViewSetPlain
- **Location**: `base.py`
- **Purpose**: Ready-to-use base viewset
- **Includes**: Permission + Serializer dynamic selection

### PartialUpdateModelMixin
- **Location**: `mixins.py`
- **Purpose**: PATCH request handling with cache invalidation
- **Methods**: `partial_update()`, `perform_update()`

### GetSerializerClassMixin
- **Location**: `mixins.py`
- **Purpose**: Action-based serializer selection
- **Config**: `serializer_action_classes = {'action': SerializerClass}`

### GetPermissionClassesMixin
- **Location**: `mixins.py`
- **Purpose**: Action-based permission selection
- **Config**: `permission_action_classes = {'action': [PermissionClass()]}`

## Usage Patterns

### Pattern 1: Complete ViewSet
```python
class TaskViewSet(BaseModelViewSetPlain, ModelViewSet):
    # Base configuration
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    # Dynamic overrides
    serializer_action_classes = {'create': CreateTaskSerializer}
    permission_action_classes = {'destroy': [IsAdminUser()]}
```

### Pattern 2: Custom Mixin Combination
```python
from .mixins import PartialUpdateModelMixin, GetSerializerClassMixin

class CustomViewSet(PartialUpdateModelMixin, GetSerializerClassMixin, GenericViewSet):
    # Only partial update + dynamic serializers
    pass
```

### Pattern 3: Individual Mixin
```python
from .mixins import GetPermissionClassesMixin

class PermissionViewSet(GetPermissionClassesMixin, ModelViewSet):
    # Only dynamic permissions
    permission_action_classes = {'create': [IsAdminUser()]}
```

## Method Reference

| Method | Mixin | Purpose |
|--------|-------|---------|
| `get_serializer_class()` | GetSerializerClassMixin | Returns action-specific serializer |
| `get_permissions()` | GetPermissionClassesMixin | Returns action-specific permissions |
| `partial_update()` | PartialUpdateModelMixin | Handles PATCH requests |
| `perform_update()` | PartialUpdateModelMixin | Executes update operation |

## Configuration

### serializer_action_classes
```python
serializer_action_classes = {
    'create': CreateSerializer,
    'update': UpdateSerializer,
    'custom_action': CustomSerializer,
}
```

### permission_action_classes
```python
permission_action_classes = {
    'create': [IsAdminUser()],
    'list': [IsAuthenticated()],
    'destroy': [IsAdminUser(), IsOwner()],
}
```

## Special Notes

- **"me" action**: GetPermissionClassesMixin skips custom permissions for "me" action
- **Cache handling**: PartialUpdateModelMixin automatically invalidates prefetch cache
- **Fallback behavior**: All mixins fall back to default DRF behavior when no custom config found
- **Debug logging**: GetPermissionClassesMixin logs current action (should be removed in production)

## Dependencies

- Django REST Framework
- Django
- Python 3.x