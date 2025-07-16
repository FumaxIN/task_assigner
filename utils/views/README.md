# Utils/Views - Django REST Framework Utilities

This directory contains utility classes and mixins for Django REST Framework (DRF) views, providing common functionality for API endpoints in the task assigner application.

## Table of Contents

- [Overview](#overview)
- [Components](#components)
- [Usage Examples](#usage-examples)
- [Installation](#installation)
- [API Reference](#api-reference)

## Overview

The `utils/views` module provides reusable components for DRF viewsets, including:

- Dynamic serializer class selection based on action
- Dynamic permission class selection based on action
- Partial update functionality with cache invalidation
- Base viewset combining common mixins

## Components

### BaseModelViewSetPlain

A base viewset class that combines common mixins for DRF viewsets.

**Location**: `base.py`

**Inherits from**:
- `GetPermissionClassesMixin`
- `GetSerializerClassMixin`
- `rest_framework.viewsets.GenericViewSet`

### Mixins

#### PartialUpdateModelMixin

Provides partial update functionality for model instances with proper cache invalidation.

**Location**: `mixins.py`

**Methods**:
- `perform_update(serializer)`: Executes the update operation
- `partial_update(request, *args, **kwargs)`: Handles PATCH requests for partial updates

#### GetSerializerClassMixin

Enables dynamic serializer class selection based on the current action.

**Location**: `mixins.py`

**Key Features**:
- Action-based serializer selection
- Fallback to default serializer class
- Support for `serializer_action_classes` attribute

#### GetPermissionClassesMixin

Allows dynamic permission class selection based on the current action.

**Location**: `mixins.py`

**Key Features**:
- Action-based permission selection
- Special handling for "me" action
- Fallback to default permission classes
- Support for `permission_action_classes` attribute

## Usage Examples

### Basic ViewSet with Dynamic Serializers

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .base import BaseModelViewSetPlain

class TaskViewSet(BaseModelViewSetPlain, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # Define action-specific serializers
    serializer_action_classes = {
        'create': CreateTaskSerializer,
        'update': UpdateTaskSerializer,
        'assign': AssignTaskSerializer,
    }
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        # This will automatically use AssignTaskSerializer
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        # ... rest of the logic
```

### Dynamic Permissions Example

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .base import BaseModelViewSetPlain

class UserViewSet(BaseModelViewSetPlain, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    # Define action-specific permissions
    permission_action_classes = {
        'create': [IsAdminUser()],
        'destroy': [IsAdminUser()],
        'list': [IsAuthenticated()],
    }
```

### Using PartialUpdateModelMixin

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from .mixins import PartialUpdateModelMixin

class CustomViewSet(PartialUpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    
    # The partial_update method is automatically available
    # Handles PATCH requests with proper cache invalidation
```

## Installation

These utilities are part of the task assigner application and don't require separate installation. They depend on Django REST Framework.

**Requirements**:
- Django REST Framework
- Python 3.x
- Django

## API Reference

### BaseModelViewSetPlain

**Class**: `BaseModelViewSetPlain`

Combines `GetPermissionClassesMixin`, `GetSerializerClassMixin`, and `GenericViewSet`.

### PartialUpdateModelMixin

**Methods**:

#### `perform_update(serializer)`
- **Parameters**: `serializer` - DRF serializer instance
- **Returns**: None
- **Description**: Executes the update operation using the serializer

#### `partial_update(request, *args, **kwargs)`
- **Parameters**: 
  - `request` - HTTP request object
  - `*args` - Additional positional arguments
  - `**kwargs` - Additional keyword arguments
- **Returns**: `Response` - DRF Response object with serialized data
- **Description**: Handles PATCH requests for partial model updates with cache invalidation

### GetSerializerClassMixin

**Methods**:

#### `get_serializer_class()`
- **Returns**: Serializer class
- **Description**: Returns the appropriate serializer class based on the current action

**Configuration**:
- **Attribute**: `serializer_action_classes` - Dictionary mapping action names to serializer classes

### GetPermissionClassesMixin

**Methods**:

#### `get_permissions()`
- **Returns**: Tuple of permission class instances
- **Description**: Returns the appropriate permission classes based on the current action

**Configuration**:
- **Attribute**: `permission_action_classes` - Dictionary mapping action names to permission class instances

**Special Behavior**:
- The "me" action falls back to default permissions
- Includes debug logging for the current action

## Notes

- The `GetPermissionClassesMixin` includes debug logging that prints the current action
- Cache invalidation is handled automatically in `PartialUpdateModelMixin`
- All mixins provide fallback behavior to default DRF methods
- The base viewset can be extended with additional DRF mixins as needed

## Contributing

When extending these utilities:

1. Maintain backward compatibility
2. Follow Django REST Framework conventions
3. Add appropriate documentation
4. Test with various DRF configurations
5. Consider performance implications of dynamic class selection