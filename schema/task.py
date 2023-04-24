from marshmallow import Schema, fields, validates, ValidationError


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    status = fields.String(required=True)
    priority = fields.String(required=True)
    due_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('status')
    def validate_status(self, value):
        if value not in ['to_do', 'in_progress', 'completed']:
            raise ValidationError('Invalid status. Status must be one of "to_do", "in_progress", or "completed".')

    @validates('priority')
    def validate_priority(self, value):
        if value not in ['low', 'medium', 'high']:
            raise ValidationError('Invalid priority. Priority must be one of "low", "medium", or "high".')
