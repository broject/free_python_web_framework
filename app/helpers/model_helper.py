from sqlalchemy import text


def _create_main_entities(op, sa):
    op.create_table('company',
                    sa.Column('id', sa.Integer),
                    sa.Column('user_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('sphere_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('business_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('reg_number', sa.String(
                        50), index=True, unique=True),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'], 'fk_company_user_id'),
                    sa.ForeignKeyConstraint(
                        ['sphere_id'], ['sphere.id'], 'fk_company_sphere_id'),
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
                    sa.Column('weblink', sa.String(1000)),
                    sa.Column('address', sa.String(500)),
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
                    sa.Column('email', sa.String(150), index=True),
                    sa.Column('phone', sa.String(150), index=True),
                    sa.Column('fax', sa.String(150), index=True),
                    sa.Column('weblink', sa.String(1000)),
                    sa.Column('address', sa.String(500)),
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
                    sa.Column('options', sa.Text),
                    sa.ForeignKeyConstraint(
                        ['branch_id'], ['branch.id'], 'fk_branch_member_branch_id'),
                    sa.ForeignKeyConstraint(
                        ['member_id'], ['user.id'], 'fk_branch_member_member_id'),
                    sa.ForeignKeyConstraint(
                        ['role_id'], ['role.id'], 'fk_branch_member_role_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('branch_member', op, sa)

    op.create_table('branch_zone',
                    sa.Column('id', sa.Integer),
                    sa.Column('branch_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('zone_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('options', sa.Text),
                    sa.ForeignKeyConstraint(
                        ['branch_id'], ['branch.id'], 'fk_branch_zone_branch_id'),
                    sa.ForeignKeyConstraint(
                        ['zone_id'], ['zone.id'], 'fk_branch_zone_zone_id'),
                    sa.UniqueConstraint(
                        'branch_id', 'zone_id', name='uq_branch_zone'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('branch_zone', op, sa)

    op.create_table('company_customer',
                    sa.Column('id', sa.Integer),
                    sa.Column('company_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('customer_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('options', sa.Text),
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

    op.create_table('branch_goods',
                    sa.Column('id', sa.Integer),
                    sa.Column('company_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('branch_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('goods_id', sa.Integer,
                              nullable=False, index=True),
                    sa.ForeignKeyConstraint(
                        ['company_id'], ['company.id'], 'fk_branch_goods_company_id'),
                    sa.ForeignKeyConstraint(
                        ['branch_id'], ['branch.id'], 'fk_branch_goods_branch_id'),
                    sa.ForeignKeyConstraint(
                        ['goods_id'], ['goods.id'], 'fk_branch_goods_goods_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('branch_goods', op, sa)

    op.create_table('branch_price',
                    sa.Column('id', sa.Integer),
                    sa.Column('branchgoods_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('price', sa.Float, nullable=False, default=0),
                    sa.Column('price_cond', sa.String(500)),
                    sa.Column('wprice', sa.Float, nullable=False, default=0),
                    sa.Column('wprice_cond', sa.String(500)),
                    sa.Column('isdefault', sa.Boolean,
                              nullable=False, default=True),
                    sa.ForeignKeyConstraint(
                        ['branchgoods_id'], ['branch_goods.id'], 'fk_branch_price_branchgoods_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('branch_price', op, sa)


def _drop_main_entities(op):
    op.drop_constraint('fk_branch_price_branchgoods_id',
                       'branch_price', type_='foreignkey')
    op.drop_table('branch_price')

    op.drop_constraint('fk_branch_goods_company_id',
                       'branch_goods', type_='foreignkey')
    op.drop_constraint('fk_branch_goods_branch_id',
                       'branch_goods', type_='foreignkey')
    op.drop_constraint('fk_branch_goods_goods_id',
                       'branch_goods', type_='foreignkey')
    op.drop_table('branch_goods')

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

    op.drop_constraint('fk_branch_zone_branch_id',
                       'branch_zone', type_='foreignkey')
    op.drop_constraint('fk_branch_zone_zone_id',
                       'branch_zone', type_='foreignkey')
    op.drop_table('branch_zone')

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
    op.drop_constraint('fk_company_sphere_id', 'company', type_='foreignkey')
    op.drop_table('company')


def _create_goods_entities(op, sa):
    op.create_table('category',
                    sa.Column('id', sa.Integer),
                    sa.Column('parent_id', sa.Integer, index=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.ForeignKeyConstraint(
                        ['parent_id'], ['category.id'], 'fk_category_parent_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('category', op, sa)

    op.create_table('category_tag',
                    sa.Column('category_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('tag_id', sa.Integer,
                              nullable=False, index=True),
                    sa.ForeignKeyConstraint(
                        ['category_id'], ['category.id'], 'fk_category_tag_category_id'),
                    sa.ForeignKeyConstraint(
                        ['tag_id'], ['tag.id'], 'fk_category_tag_tag_id'),
                    sa.UniqueConstraint(
                        'category_id', 'tag_id', name='uq_category_tag')
                    )

    op.create_table('goods',
                    sa.Column('id', sa.Integer),
                    sa.Column('barcode', sa.String(128),
                              nullable=False, index=True, unique=True),
                    sa.Column('longcode', sa.String(30), index=True),
                    sa.Column('qrcode', sa.Text),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('descr', sa.String(500)),
                    sa.Column('category_id', sa.Integer, index=True),
                    sa.Column('thumb_id', sa.Integer, index=True),
                    sa.Column('package_id', sa.Integer, index=True),
                    # нэгж >>
                    # piece_value = 10, piece_unit_id = ширхэг
                    # piece_value = 50, piece_unit_id = ширхэг
                    sa.Column('piece_unit_id', sa.Integer, index=True),
                    sa.Column('piece_value', sa.Float,
                              nullable=False, default=0),
                    # жин >>
                    # weight_value = 0.5, weight_unit_id = килограмм
                    # weight_value = 500, weight_unit_id = грамм
                    sa.Column('weight_unit_id', sa.Integer, index=True),
                    sa.Column('weight_value', sa.Float,
                              nullable=False, default=0),
                    # эзэлхүүн >>
                    # cubature_value = 330, cubature_unit_id = миллилитр
                    sa.Column('cubature_unit_id', sa.Integer, index=True),
                    sa.Column('cubature_value', sa.Float,
                              nullable=False, default=0),
                    # үнэ
                    sa.Column('particle_price', sa.Float,
                              nullable=False, default=0),
                    # бөөний үнэ
                    sa.Column('wholesale_price', sa.Float,
                              nullable=False, default=0),
                    # бөөний үнийн нөхцөл
                    sa.Column('wholesale_cond', sa.String(500)),
                    sa.ForeignKeyConstraint(
                        ['category_id'], ['category.id'], 'fk_goods_category_id'),
                    sa.ForeignKeyConstraint(
                        ['thumb_id'], ['media.id'], 'fk_goods_thumb_id'),
                    sa.ForeignKeyConstraint(
                        ['package_id'], ['package.id'], 'fk_goods_package_id'),
                    sa.ForeignKeyConstraint(
                        ['piece_unit_id'], ['unit.id'], 'fk_goods_piece_unit_id'),
                    sa.ForeignKeyConstraint(
                        ['weight_unit_id'], ['unit.id'], 'fk_goods_weight_unit_id'),
                    sa.ForeignKeyConstraint(
                        ['cubature_unit_id'], ['unit.id'], 'fk_goods_cubature_unit_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('goods', op, sa)

    op.create_table('goods_tag',
                    sa.Column('goods_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('tag_id', sa.Integer,
                              nullable=False, index=True),
                    sa.ForeignKeyConstraint(
                        ['goods_id'], ['goods.id'], 'fk_goods_tag_goods_id'),
                    sa.ForeignKeyConstraint(
                        ['tag_id'], ['tag.id'], 'fk_goods_tag_tag_id'),
                    sa.UniqueConstraint(
                        'goods_id', 'tag_id', name='uq_goods_tag')
                    )

    op.create_table('goods_category',
                    sa.Column('goods_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('category_id', sa.Integer,
                              nullable=False, index=True),
                    sa.ForeignKeyConstraint(
                        ['goods_id'], ['goods.id'], 'fk_goods_category_goods_id'),
                    sa.ForeignKeyConstraint(
                        ['category_id'], ['category.id'], 'fk_goods_category_category_id'),
                    sa.UniqueConstraint(
                        'goods_id', 'category_id', name='uq_goods_category')
                    )

    op.create_table('goods_detail',
                    sa.Column('id', sa.Integer),
                    sa.Column('goods_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('item_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('value', sa.String(255), index=True),
                    sa.Column('data', sa.Text),
                    sa.ForeignKeyConstraint(
                        ['goods_id'], ['goods.id'], 'fk_goods_detail_goods_id'),
                    sa.ForeignKeyConstraint(
                        ['item_id'], ['item.id'], 'fk_goods_detail_item_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('goods_detail', op, sa)

    op.create_table('goods_media',
                    sa.Column('id', sa.Integer),
                    sa.Column('goods_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('media_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('title', sa.String(255)),
                    sa.Column('data', sa.Text),
                    sa.ForeignKeyConstraint(
                        ['goods_id'], ['goods.id'], 'fk_goods_media_goods_id'),
                    sa.ForeignKeyConstraint(
                        ['media_id'], ['media.id'], 'fk_goods_media_media_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('goods_media', op, sa)


def _drop_goods_entities(op):
    op.drop_constraint('fk_goods_media_goods_id',
                       'goods_media', type_='foreignkey')
    op.drop_constraint('fk_goods_media_media_id',
                       'goods_media', type_='foreignkey')
    op.drop_table('goods_media')

    op.drop_constraint('fk_goods_detail_goods_id',
                       'goods_detail', type_='foreignkey')
    op.drop_constraint('fk_goods_detail_item_id',
                       'goods_detail', type_='foreignkey')
    op.drop_table('goods_detail')

    op.drop_constraint('fk_goods_category_goods_id',
                       'goods_category', type_='foreignkey')
    op.drop_constraint('fk_goods_category_category_id',
                       'goods_category', type_='foreignkey')
    op.drop_table('goods_category')

    op.drop_constraint('fk_goods_tag_goods_id',
                       'goods_tag', type_='foreignkey')
    op.drop_constraint('fk_goods_tag_tag_id',
                       'goods_tag', type_='foreignkey')
    op.drop_table('goods_tag')

    op.drop_constraint('fk_goods_cubature_unit_id',
                       'goods', type_='foreignkey')
    op.drop_constraint('fk_goods_weight_unit_id',
                       'goods', type_='foreignkey')
    op.drop_constraint('fk_goods_piece_unit_id',
                       'goods', type_='foreignkey')
    op.drop_constraint('fk_goods_package_id',
                       'goods', type_='foreignkey')
    op.drop_constraint('fk_goods_thumb_id',
                       'goods', type_='foreignkey')
    op.drop_constraint('fk_goods_category_id',
                       'goods', type_='foreignkey')
    op.drop_table('goods')

    op.drop_constraint('fk_category_tag_category_id',
                       'category_tag', type_='foreignkey')
    op.drop_constraint('fk_category_tag_tag_id',
                       'category_tag', type_='foreignkey')
    op.drop_table('category_tag')

    op.drop_constraint('fk_category_parent_id',
                       'category', type_='foreignkey')
    op.drop_table('category')


def _create_necessary_entities(op, sa):
    op.create_table('settings',
                    sa.Column('id', sa.Integer),
                    sa.Column('section', sa.String(150),
                              index=True, unique=True),
                    sa.Column('code', sa.String(150), nullable=False,
                              index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('value', sa.Text),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('settings', op, sa)

    op.create_table('zone',
                    sa.Column('id', sa.Integer),
                    sa.Column('user_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('code', sa.String(150), index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('data', sa.Text),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'], 'fk_zone_user_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('zone', op, sa)

    op.create_table('package',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(150), index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('package', op, sa)

    op.create_table('item',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(150), index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('item', op, sa)

    op.create_table('tag',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(150), index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('tag', op, sa)

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
                    sa.Column('code', sa.String(30),
                              nullable=False, index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('unit', op, sa)

    op.create_table('quality',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(150), index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('quality', op, sa)

    op.create_table('sphere',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('name', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    upgrade_base_columns('sphere', op, sa)

    op.create_table('business',
                    sa.Column('id', sa.Integer),
                    sa.Column('code', sa.String(150), index=True, unique=True),
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
                              nullable=False, default='/'),
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


def _drop_necessary_entities(op):
    op.drop_constraint('fk_media_mediafolder_id', 'media', type_='foreignkey')
    op.drop_constraint('fk_media_mediatype_id', 'media', type_='foreignkey')
    op.drop_table('media')
    op.drop_table('mediatype')
    op.drop_constraint('fk_mediafolder_parent_id',
                       'mediafolder', type_='foreignkey')
    op.drop_table('mediafolder')

    op.drop_table('business')
    op.drop_table('sphere')
    op.drop_table('gender')
    op.drop_table('unit')
    op.drop_table('quality')
    op.drop_table('tag')
    op.drop_table('item')
    op.drop_table('package')
    op.drop_constraint('fk_zone_user_id',
                       'zone', type_='foreignkey')
    op.drop_table('zone')
    op.drop_table('settings')


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
                    sa.Column('username', sa.String(50),
                              nullable=False, index=True, unique=True),
                    sa.Column('email', sa.String(150),
                              nullable=False, index=True, unique=True),
                    sa.Column('phone', sa.String(150), index=True),
                    sa.Column('password_salt', sa.String(255)),
                    sa.Column('password_hash', sa.String(255)),
                    sa.Column('role_id', sa.Integer,
                              nullable=False, index=True),
                    sa.Column('first_name', sa.String(50), index=True),
                    sa.Column('last_name', sa.String(50), index=True),
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


# call in the alembic first migration
def upgrade_default_entities(op, sa):
    _create_auth_entities(op, sa)
    _create_necessary_entities(op, sa)
    _create_goods_entities(op, sa)
    _create_main_entities(op, sa)


# call in the alembic first migration
def downgrade_default_entities(op):
    _drop_main_entities(op)
    _drop_goods_entities(op)
    _drop_necessary_entities(op)
    _drop_auth_entities(op)


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
