# Database Migrations

> **Keywords:** make migration, run migrations, rollback migration, schema changes, database versioning, migration tool

Asok includes a professional, version-controlled migration system that allows you to manage your database schema evolution with confidence. It features **automatic change detection**, batch tracking, and atomic rollbacks.

## 1. Concept

Instead of modifying your database manually or relying solely on automatic schema updates, you define your schema in your **Models**. Asok then detects the differences between your code and the actual database state, generating versioned migration files in `src/migrations/`.

## 2. Generating Migrations

When you add a new model or modify an existing one (adding fields), run the following command:

```bash
asok make migration add_phone_to_users
```

Asok will perform a deep analysis of your models and current database schema, then create a file like `src/migrations/0001_add_phone_to_users.py`.

### What Asok Detects
- **New Tables**: Automatically generates `CreateModel` operations with all fields, constraints, default values, and relations.
- **New Columns**: Detects missing columns in existing models and generates `AddField` operations.
- **Removed Columns**: Detects deleted columns in models and generates `RemoveField` operations.
- **Altered Columns**: Detects type or constraint updates and generates `AlterField` operations.
- **Renamed Columns**: Detects column name changes and generates `RenameField` operations.

### Anatomy of a Migration File
Starting with version `v0.5.0`, Asok uses declarative migrations. A migration file defines a subclass of `Migration` containing:
- `dependencies`: A list of preceding migration names that must be applied first.
- `operations`: A list of declarative operations executed sequentially when migrating forwards, or in reverse order when rolling back.

Here is an example of an initial migration file generating the database schema:

```python
"""
Asok Migration: auto_migration
Generated at: 2026-06-21 03:15:01
"""

from asok import Migration, operations

class Migration(Migration):
    dependencies = [
        
    ]

    operations = [
        operations.CreateModel(
        name='Address',
        table='addresses',
        fields={'user_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'label': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'street': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'city': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': 'Paris', 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'postal_code': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': '75000', 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'country': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': 'France', 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'is_default': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': False, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': True, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'user': {'type': 'BelongsTo', 'target_model_name': 'User', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    ),
        operations.CreateModel(
        name='AdminLog',
        table='admin_logs',
        fields={'user_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'action': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'entity': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'entity_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'changes': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Cart',
        table='carts',
        fields={'user_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'coupon_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'user': {'type': 'BelongsTo', 'target_model_name': 'User', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}, 'coupon': {'type': 'BelongsTo', 'target_model_name': 'Coupon', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}, 'items': {'type': 'HasMany', 'target_model_name': 'CartItem', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    ),
        operations.CreateModel(
        name='CartItem',
        table='cart_items',
        fields={'cart_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'product_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'quantity': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': 1, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'cart': {'type': 'BelongsTo', 'target_model_name': 'Cart', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}, 'product': {'type': 'BelongsTo', 'target_model_name': 'Product', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Category',
        table='categories',
        fields={'name': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'slug': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': True, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'description': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'image': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={},
        search_fields=[],
    ),
        operations.CreateModel(
        name='ContactMessage',
        table='contact_messages',
        fields={'name': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'email': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'subject': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'message': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Coupon',
        table='coupons',
        fields={'code': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': True, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'discount_type': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': 'percentage', 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'discount_value': {'type': 'Field', 'sql_type': 'REAL', 'nullable': False, 'default': 0.0, 'unique': False, 'max_length': None, 'precision': 2, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'expires_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': True, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'is_active': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': True, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': True, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Newsletter',
        table='newsletters',
        fields={'email': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': True, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Order',
        table='orders',
        fields={'user_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'subtotal': {'type': 'Field', 'sql_type': 'REAL', 'nullable': False, 'default': 0.0, 'unique': False, 'max_length': None, 'precision': 2, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'discount_amount': {'type': 'Field', 'sql_type': 'REAL', 'nullable': True, 'default': 0, 'unique': False, 'max_length': None, 'precision': 2, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'total_amount': {'type': 'Field', 'sql_type': 'REAL', 'nullable': False, 'default': 0.0, 'unique': False, 'max_length': None, 'precision': 2, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'coupon_code': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'status': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': 'pending', 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'address': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'tracking_number': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'shipping_method': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': 'Standard Shipping', 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'updated_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'user': {'type': 'BelongsTo', 'target_model_name': 'User', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}, 'items': {'type': 'HasMany', 'target_model_name': 'OrderItem', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    ),
        operations.CreateModel(
        name='OrderItem',
        table='order_items',
        fields={'order_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'product_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'price': {'type': 'Field', 'sql_type': 'REAL', 'nullable': False, 'default': 0.0, 'unique': False, 'max_length': None, 'precision': 2, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'quantity': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': 1, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'order': {'type': 'BelongsTo', 'target_model_name': 'Order', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}, 'product': {'type': 'BelongsTo', 'target_model_name': 'Product', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Product',
        table='products',
        fields={'name': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'slug': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': True, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'description': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'price': {'type': 'Field', 'sql_type': 'REAL', 'nullable': False, 'default': 0.0, 'unique': False, 'max_length': None, 'precision': 2, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'stock': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': 0, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'image_1': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'image_2': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'image_3': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'category_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'updated_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'category': {'type': 'BelongsTo', 'target_model_name': 'Category', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=['name', 'description'],
    ),
        operations.CreateModel(
        name='Review',
        table='reviews',
        fields={'user_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'product_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'rating': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': 5, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'comment': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'user': {'type': 'BelongsTo', 'target_model_name': 'User', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}, 'product': {'type': 'BelongsTo', 'target_model_name': 'Product', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Role',
        table='roles',
        fields={'name': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': True, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'label': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'permissions': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': '', 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={},
        search_fields=[],
    ),
        operations.CreateModel(
        name='User',
        table='users',
        fields={'username': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': True, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'email': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': True, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'password': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'name': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'avatar': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'is_admin': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': True, 'default': False, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': True, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'reset_token': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': 255, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'reset_token_expires': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': True, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'roles': {'type': 'BelongsToMany', 'target_model_name': 'Role', 'pivot_table': 'role_user', 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    ),
        operations.CreateModel(
        name='Wishlist',
        table='wishlist',
        fields={'user_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'product_id': {'type': 'Field', 'sql_type': 'INTEGER', 'nullable': False, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}, 'created_at': {'type': 'Field', 'sql_type': 'TEXT', 'nullable': True, 'default': None, 'unique': False, 'max_length': None, 'precision': None, 'is_boolean': False, 'is_json': False, 'is_uuid': False, 'is_datetime': False, 'is_date': False, 'is_time': False, 'is_vector': False, 'dimensions': None}},
        relations={'user': {'type': 'BelongsTo', 'target_model_name': 'User', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}, 'product': {'type': 'BelongsTo', 'target_model_name': 'Product', 'pivot_table': None, 'pivot_fk': None, 'pivot_other_fk': None}},
        search_fields=[],
    )
    ]
```

And here is an example of a subsequent migration that modifies the schema (e.g., renaming a field) and depends on the first migration:

```python
"""
Asok Migration: auto_migration
Generated at: 2026-06-21 03:18:14
"""

from asok import Migration, operations

class Migration(Migration):
    dependencies = [
        '0001_auto_migration'
    ]

    operations = [
        operations.RenameField(
        model_name='ContactMessage',
        old_name='name',
        new_name='nom',
    )
    ]
```


## 3. Applying Migrations

To apply all pending migrations:

```bash
asok migrate
```

### Specifying a Database

You can apply migrations to a specific database backend by using the `--database` option (accepts a configured database name or a DSN connection string):

```bash
asok migrate --database=read_replica
```

Asok tracks applied migrations in a special `_asok_migrations` table. Migrations are executed in **batches**. All migrations run in a single `asok migrate` call belong to the same batch.

## 4. Checking Status

To see the history of applied migrations and what is pending:

```bash
asok migrate --status
```

Output example:
```text
MIGRATION STATUS
  [X] 0001_initial_schema
  [X] 0002_add_user_bio
  [ ] 0003_create_posts_table
```

## 5. Rolling Back & Target Migrations

Asok provides flexible options to undo schema changes, target specific versions, or reset the database completely:

### Revert the last batch
By default, rolling back reverts the most recent batch of migrations:
```bash
asok migrate --rollback
```
This will execute the database rollback operations of every migration in the most recent batch and remove them from the tracking table.

### Revert a specific number of migrations
You can specify exactly how many migrations you want to roll back (regardless of their batch number) using `--steps`:
```bash
asok migrate --rollback --steps 3
```

### Migrate or Rollback to a specific version
You can force the database to align with a specific migration name or prefix using `--to`. If the target migration is currently applied, Asok will roll back any migrations applied *after* it. If it is pending, Asok will apply all migrations *up to and including* it:
```bash
asok migrate --to=0002_add_user_bio
```

### Reset all migrations
To rollback all applied migrations in reverse chronological order and return to an empty database state:
```bash
asok migrate --reset
```

## 6. Advanced Options

### Faking Migrations
If your database is out of sync but the schema is correct, you can "fake" a migration:

```bash
asok migrate --fake
```

This marks pending migrations as applied in the tracking table without actually running the SQL. It also works with `--rollback`.

## 7. Production Workflow (Best Practices)

To ensure the stability and reliability of your production database, always follow this workflow:

1.  **Generate in Dev**: Run `asok make migration` on your development machine.
2.  **Ship in Build**: Run `asok build` to include these migrations in your distribution.
3.  **Apply in Prod**: Run `asok migrate` on your production server.

> **Do not run `asok make migration` in production.** Your distribution should be considered immutable; migrations should be authored in development and deployed as part of your release.

> Always review generated migration files before applying them, especially in production environments.
