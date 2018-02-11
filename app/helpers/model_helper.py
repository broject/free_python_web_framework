from sqlalchemy import text


def _create_main_entities(op, sa):
    op.create_table('company',
                    sa.Column('id', sa.Integer),
                    sa.Column('user_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('business_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('reg_number', sa.String(60),
                              nullable=False, index=True, unique=True),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'], 'fk_company_user_id'),
                    sa.ForeignKeyConstraint(
                        ['business_id'], ['business.id'], 'fk_company_business_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('company', op, sa)

    op.create_table('company_info',
                    sa.Column('id', sa.Integer),
                    sa.Column('company_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('avatar_id', sa.Integer, index=True),
                    sa.Column('cover_id', sa.Integer, index=True),
                    sa.Column('short_name', sa.String(150), index=True),
                    sa.Column('inter_name', sa.String(150), index=True),
                    sa.Column('email', sa.String(150), index=True),
                    sa.Column('phone', sa.String(150), index=True),
                    sa.Column('fax', sa.String(150), index=True),
                    sa.Column('website', sa.String(150), index=True),
                    sa.Column('overview', sa.Text),
                    sa.Column('policy', sa.Text),
                    sa.Column('mission', sa.Text),
                    sa.Column('vision', sa.Text),
                    sa.Column('contents', sa.Text),
                    sa.ForeignKeyConstraint(
                        ['company_id'], ['company.id'], 'fk_company_info_company_id'),
                    sa.ForeignKeyConstraint(
                        ['avatar_id'], ['media.id'], 'fk_company_info_avatar_id'),
                    sa.ForeignKeyConstraint(
                        ['cover_id'], ['media.id'], 'fk_company_info_cover_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('company_info', op, sa)

    op.create_table('branch',
                    sa.Column('id', sa.Integer),
                    sa.Column('company_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.ForeignKeyConstraint(
                        ['company_id'], ['company.id'], 'fk_branch_company_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('branch', op, sa)

    op.create_table('branch_member',
                    sa.Column('id', sa.Integer),
                    sa.Column('branch_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('member_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('role_id', sa.Integer,
                              nullable=False, index=True),
                    sa.ForeignKeyConstraint(
                        ['branch_id'], ['branch.id'], 'fk_branch_member_branch_id'),
                    sa.ForeignKeyConstraint(
                        ['member_id'], ['user.id'], 'fk_branch_member_member_id'),
                    sa.ForeignKeyConstraint(
                        ['role_id'], ['role.id'], 'fk_branch_member_role_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('branch_member', op, sa)

    op.create_table('company_customer',
                    sa.Column('id', sa.Integer),
                    sa.Column('company_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('customer_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('data', sa.Text),
                    sa.ForeignKeyConstraint(
                        ['company_id'], ['company.id'], 'fk_company_customer_company_id'),
                    sa.ForeignKeyConstraint(
                        ['customer_id'], ['company.id'], 'fk_company_customer_customer_id'),
                    sa.UniqueConstraint(
                        'company_id', 'customer_id', name='uq_company_customer'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('company_customer', op, sa)

    op.create_table('branch_customer',
                    sa.Column('branch_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('customer_id', sa.Integer,
                              nullable=False, index=True),
                    sa.ForeignKeyConstraint(
                        ['branch_id'], ['branch.id'], 'fk_branch_customer_branch_id'),
                    sa.ForeignKeyConstraint(
                        ['customer_id'], ['company.id'], 'fk_branch_customer_customer_id'),
                    sa.UniqueConstraint(
                        'branch_id', 'customer_id', name='uq_branch_customer')
                    )


def _drop_main_entities(op):
    op.drop_constraint('fk_branch_customer_branch_id',
                       'branch_customer', type_='foreignkey')
    op.drop_constraint('fk_branch_customer_customer_id',
                       'branch_customer', type_='foreignkey')
    op.drop_table('branch_customer')

    op.drop_constraint('fk_company_customer_company_id',
                       'company_customer', type_='foreignkey')
    op.drop_constraint('fk_company_customer_customer_id',
                       'company_customer', type_='foreignkey')
    op.drop_table('company_customer')

    op.drop_constraint('fk_branch_member_branch_id',
                       'branch_member', type_='foreignkey')
    op.drop_constraint('fk_branch_member_member_id',
                       'branch_member', type_='foreignkey')
    op.drop_constraint('fk_branch_member_role_id',
                       'branch_member', type_='foreignkey')
    op.drop_table('branch_member')

    op.drop_constraint('fk_branch_company_id',
                       'branch', type_='foreignkey')
    op.drop_table('branch')

    op.drop_constraint('fk_company_info_company_id',
                       'company_info', type_='foreignkey')
    op.drop_constraint('fk_company_info_avatar_id',
                       'company_info', type_='foreignkey')
    op.drop_constraint('fk_company_info_cover_id',
                       'company_info', type_='foreignkey')
    op.drop_table('company_info')

    op.drop_constraint('fk_company_user_id', 'company', type_='foreignkey')
    op.drop_constraint('fk_company_business_id', 'company', type_='foreignkey')
    op.drop_table('company')

    # _drop_necessary_entities

    op.drop_constraint('fk_media_mediafolder_id', 'media', type_='foreignkey')
    op.drop_constraint('fk_media_mediatype_id', 'media', type_='foreignkey')
    op.drop_table('media')
    op.drop_table('mediatype')
    op.drop_constraint('fk_mediafolder_parent_id',
                       'mediafolder', type_='foreignkey')
    op.drop_table('mediafolder')

    op.drop_table('business')
    op.drop_table('gender')
    op.drop_table('unit')
    op.drop_table('quality')


def _create_necessary_entities(op, sa):
    op.create_table('gender',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(30),
                              nullable=False, index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('gender', op, sa)

    op.create_table('unit',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(50),
                              nullable=False, index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('unit', op, sa)

    op.create_table('quality',
                    sa.Column('id', sa.Integer),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('quality', op, sa)

    op.create_table('business',
                    sa.Column('id', sa.Integer),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('business', op, sa)

    op.create_table('mediafolder',
                    sa.Column('id', sa.Integer),
                    sa.Column('parent_id', sa.Integer, index=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('protected', sa.Boolean,
                              nullable=False, default=False),
                    sa.ForeignKeyConstraint(
                        ['parent_id'], ['mediafolder.id'], 'fk_mediafolder_parent_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('mediafolder', op, sa)

    op.create_table('mediatype',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(50),
                              nullable=False, index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('mediatype', op, sa)

    op.create_table('media',
                    sa.Column('id', sa.Integer),
                    sa.Column('mediafolder_id', sa.Integer, index=True),
                    sa.Column('mediatype_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('title', sa.String(255)),
                    sa.Column('path', sa.String(1000),
                              nullable=False, default=''),
                    sa.Column('filename', sa.String(255), nullable=False),
                    sa.Column('extension', sa.String(30), nullable=False),
                    sa.Column('mimetype', sa.String(255), nullable=False),
                    sa.Column('size', sa.Integer, nullable=False, default=0),
                    sa.Column('width', sa.Integer, nullable=False, default=0),
                    sa.Column('height', sa.Integer, nullable=False, default=0),
                    sa.Column('duration', sa.Integer,
                              nullable=False, default=0),
                    sa.Column('protected', sa.Boolean,
                              nullable=False, default=False),
                    sa.ForeignKeyConstraint(
                        ['mediafolder_id'], ['mediafolder.id'], 'fk_media_mediafolder_id'),
                    sa.ForeignKeyConstraint(
                        ['mediatype_id'], ['mediatype.id'], 'fk_media_mediatype_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('media', op, sa)


def _create_auth_entities(op, sa):
    op.create_table('role',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.Integer, nullable=False,
                              index=True, unique=True),
                    sa.Column('name', sa.String(150), nullable=False,
                              index=True, unique=True),
                    sa.Column('title', sa.String(255)),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('role', op, sa)

    op.create_table('permission',
                    sa.Column('id', sa.Integer),
                    sa.Column('name', sa.String(150),
                              nullable=False, unique=True),
                    sa.Column('descr', sa.String(500)),
                    sa.Column('data', sa.Text),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('permission', op, sa)

    op.create_table('role_permission',
                    sa.Column('role_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('permission_id', sa.Integer,
                              nullable=False, index=True),
                    sa.ForeignKeyConstraint(
                        ['role_id'], ['role.id'], 'fk_role_permission_role_id'),
                    sa.ForeignKeyConstraint(
                        ['permission_id'], ['permission.id'], 'fk_role_permission_permission_id'),
                    sa.UniqueConstraint(
                        'role_id', 'permission_id', name='uq_role_permission')
                    )

    op.create_table('user',
                    sa.Column('id', sa.Integer),
                    sa.Column('username', sa.String(60),
                              nullable=False, index=True, unique=True),
                    sa.Column('email', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('phone', sa.String(150), index=True),
                    sa.Column('password_salt', sa.String(255)),
                    sa.Column('password_hash', sa.String(255)),
                    sa.Column('role_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('first_name', sa.String(60), index=True),
                    sa.Column('last_name', sa.String(60), index=True),
                    sa.ForeignKeyConstraint(
                        ['role_id'], ['role.id'], 'fk_user_role_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('user', op, sa)

    op.create_table('client',
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True),
                    sa.Column('client_id', sa.String(50)),
                    sa.Column('client_secret', sa.String(255),
                              nullable=False, index=True, unique=True),
                    sa.Column('client_type', sa.String(50),
                              nullable=False, default='public'),
                    sa.Column('default_scope', sa.String(500),
                              nullable=False, default='email address'),
                    sa.Column('redirect_uris', sa.Text),
                    sa.PrimaryKeyConstraint('client_id')
                    )

    op.create_table('grunt',
                    sa.Column('id', sa.Integer),
                    sa.Column('client_id', sa.String(50),
                              nullable=False, index=True),
                    sa.Column('user_id', sa.Integer,
                              nullable=True, index=True),
                    sa.Column('code', sa.String(255), nullable=False,
                              index=True, unique=True),
                    sa.Column('redirect_uri', sa.String(1000)),
                    sa.Column('scope', sa.String(500)),
                    sa.Column('expires', sa.DateTime),
                    sa.ForeignKeyConstraint(
                        ['client_id'], ['client.client_id'], 'fk_grunt_client_id', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'], 'fk_grunt_user_id', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('grunt', op, sa)

    op.create_table('token',
                    sa.Column('id', sa.Integer),
                    sa.Column('client_id', sa.String(50),
                              nullable=False, index=True),
                    sa.Column('user_id', sa.Integer,
                              nullable=True, index=True),
                    sa.Column('token_type', sa.String(50)),
                    sa.Column('access_token', sa.String(255)),
                    sa.Column('refresh_token', sa.String(255)),
                    sa.Column('scope', sa.String(500)),
                    sa.Column('expires', sa.DateTime),
                    sa.ForeignKeyConstraint(
                        ['client_id'], ['client.client_id'], 'fk_token_client_id', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'], 'fk_token_user_id', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('token', op, sa)


def _drop_auth_entities(op):
    op.drop_constraint('fk_token_user_id', 'token', type_='foreignkey')
    op.drop_constraint('fk_token_client_id', 'token', type_='foreignkey')
    op.drop_table('token')

    op.drop_constraint('fk_grunt_user_id', 'grunt', type_='foreignkey')
    op.drop_constraint('fk_grunt_client_id', 'grunt', type_='foreignkey')
    op.drop_table('grunt')

    op.drop_table('client')

    op.drop_constraint('fk_user_role_id', 'user', type_='foreignkey')
    op.drop_table('user')

    op.drop_constraint('fk_role_permission_role_id',
                       'role_permission', type_='foreignkey')
    op.drop_constraint('fk_role_permission_permission_id',
                       'role_permission', type_='foreignkey')
    op.drop_table('role_permission')
    op.drop_table('permission')
    op.drop_table('role')


def downgrade_default_entities(op):
    _drop_main_entities(op)
    _drop_auth_entities(op)


def upgrade_default_entities(op, sa):
    _create_auth_entities(op, sa)
    _create_necessary_entities(op, sa)
    _create_main_entities(op, sa)


def downgrade_base_columns(tablename, op):
    op.drop_column(tablename, 'deleted')
    op.drop_column(tablename, 'created_at')
    op.drop_column(tablename, 'modified_at')


def upgrade_base_columns(tablename, op, sa):
    op.add_column(tablename, sa.Column(
        'deleted', sa.Boolean, nullable=False, default=False))
    op.add_column(tablename, sa.Column(
        'created_at', sa.TIMESTAMP, nullable=False,
        server_default=text('CURRENT_TIMESTAMP')))
    op.add_column(tablename, sa.Column(
        'modified_at', sa.TIMESTAMP, nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))
