def downgrade_base_columns(tablename, op):
    op.drop_column(tablename, 'deleted')
    op.drop_column(tablename, 'created_at')
    op.drop_column(tablename, 'modified_at')


def upgrade_base_columns(tablename, op, sa):
    from sqlalchemy import text
    op.add_column(tablename, sa.Column(
        'deleted', sa.Boolean(), nullable=False, default=False))
    op.add_column(tablename, sa.Column(
        'created_at', sa.TIMESTAMP, nullable=False,
        server_default=text('CURRENT_TIMESTAMP')))
    op.add_column(tablename, sa.Column(
        'modified_at', sa.TIMESTAMP, nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))
