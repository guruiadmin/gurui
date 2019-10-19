from django.db import models

# Create your models here.


#用户名查询
class UserData(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    unionid = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    wx_nick_name = models.CharField(max_length=64)
    sex = models.SlugField(default='1')
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=64)
    is_system = models.SlugField(default='0')
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'jld_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def new_create_time(self):
        return self.create_time.strftime('%Y-%m-%d')

# 用户名查询
class EleUserData(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=64)
    wx_nick_name = models.CharField(max_length=64)
    sex = models.SlugField(default='1')
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=64)
    is_system = models.SlugField(default='0')

    class Meta:
        db_table = 'jld_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


#商家模糊查询
class ManageOrm(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    foreign_key = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    describe = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    web_site = models.CharField(max_length=255)
    status = models.SlugField(default='0')
    status_result = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    is_delete = models.SlugField(default='0')
    business_license = models.CharField(max_length=255)

    class Meta:
        db_table = 'manager'
        verbose_name = '商家'
        verbose_name_plural = verbose_name

    def new_create_time(self):
        return self.create_time.strftime('%Y-%m-%d')

# 商品属性表
class GoodsProperty(models.Model):
    goods_id = models.CharField(max_length=255, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    group_price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.SlugField(default='0')
    warning = models.SlugField(default='0')

    class Meta:
        db_table = 'goods_property'
        verbose_name = '商品属性表'
        verbose_name_plural = verbose_name

# 商品信息表
class ActivityUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    userAddr = models.CharField(max_length=255)
    goodsAddr = models.CharField(max_length=255)
    isReceive = models.SlugField(default='0')
    isRob = models.SlugField(default='0')
    isUsed = models.SlugField(default='0')

    class Meta:
        db_table = 'activity_user'
        verbose_name = '商品信息表'
        verbose_name_plural = verbose_name

#商品
class GoodsOrm(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    foreign_key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    brief = models.CharField(max_length=255)
    market_price = models.DecimalField(max_digits=10, decimal_places=2)
    presell = models.SlugField(default='0')
    putaway = models.SlugField(default='0')
    audit_result = models.SlugField(default='1')
    recommend = models.SlugField(default='0')
    guarantees = models.SlugField(default='0')
    expiration_time = models.DateTimeField()
    circulation = models.SlugField()
    oto = models.SlugField(default='0')
    is_display = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    is_represent = models.SlugField(default='0')
    favorable_price = models.SlugField(default='0.00')
    create_time = models.DateTimeField()
    sales_volume = models.SlugField(default='0')
    is_delete = models.SlugField(default='0')
    state = models.SlugField()
    represent_price = models.DecimalField(max_digits=10, decimal_places=2)
    represent_commission = models.DecimalField(max_digits=10, decimal_places=2)
    represent_rank = models.SlugField(default='0')
    represent_usercount = models.SlugField(default='0')
    initial_account = models.CharField(max_length=255)


    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def new_create_time(self):
        return self.create_time.strftime('%Y-%m-%d')

#购买订单表
class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=255, primary_key=True)
    manager_id = models.CharField(max_length=255)
    auto_take = models.SlugField(default='0')
    user_name = models.CharField(max_length=50)
    user_addr = models.CharField(max_length=50)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=50)
    order_source = models.SlugField(default='0')
    pay_state = models.SlugField(default='0')
    order_state = models.SlugField(default='0')
    consignee_user = models.CharField(max_length=50)
    consignee_phone = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    user_msg = models.TextField()
    pay_time = models.DateTimeField()

    class Meta:
        db_table = 'purchase_order'
        verbose_name = '购买订单表'
        verbose_name_plural = verbose_name

    def new_create_time(self):
        return self.create_time.strftime('%Y-%m-%d')


# 购买订单商品表
class PurchaseOorderGoods(models.Model):
    order_number = models.CharField(max_length=255, primary_key=True)
    goods_id = models.CharField(max_length=255)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_group_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_amount = models.SlugField()
    refund_amount = models.SlugField(default='0')
    # is_afert_sale = models.SlugField(default='0')
    after_sale_num = models.SlugField(default='0')
    is_coupons = models.SlugField(default='0')
    coupons_addr = models.CharField(max_length=255)
    goods_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'purchase_order_goods'
        verbose_name = '购买订单_商品表'
        verbose_name_plural = verbose_name

    def new_create_time(self):
        return self.create_time.strftime('%Y-%m-%d')

# 购买订单_快递表
class PurchaseOrderLogistics(models.Model):
    order_num = models.CharField(max_length=255, primary_key=True)
    logistics_company = models.CharField(max_length=50)
    logistice_cost = models.DecimalField(max_digits=10, decimal_places=2)
    consignee_user = models.CharField(max_length=50)
    consignee_phone = models.CharField(max_length=50)
    logistics_num = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    detail_addr = models.CharField(max_length=50)
    delivery_time = models.DateTimeField()
    received_time = models.DateTimeField()

    class Meta:
        db_table = 'purchase_order_logistics'
        verbose_name = '购买订单_快递表'
        verbose_name_plural = verbose_name

    def new_create_time(self):
        return self.create_time.strftime('%Y-%m-%d')

# 提货订单表
class TakeOrder(models.Model):
    order_number = models.CharField(max_length=255, primary_key=True)
    manager_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_addr = models.CharField(max_length=50)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    take_state = models.SlugField(default='0')
    order_state = models.SlugField(default='0')
    consignee_user = models.CharField(max_length=50)
    consignee_phone = models.CharField(max_length=50)
    create_date = models.DateTimeField()
    user_msg = models.TextField()


    class Meta:
        db_table = 'take_order'
        verbose_name = '提货订单表'
        verbose_name_plural = verbose_name

    def new_create_time(self):
        return self.create_time.strftime('%Y-%m-%d')
# 提货订单_商品表
class TakeOrderGoods(models.Model):
    order_number = models.CharField(max_length=255, primary_key=True)
    goods_id = models.CharField(max_length=255)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_group_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_amount = models.SlugField(default='0')
    refund_amount = models.SlugField(default='0')
    is_after_sale = models.SlugField(default='0')
    use_delivery = models.SlugField(default='0')
    delivery_addr = models.CharField(max_length=255)


    class Meta:
        db_table = 'take_order_goods'
        verbose_name = '提货订单表'
        verbose_name_plural = verbose_name



# 提货订单_快递表
class TakeOrderLogistics(models.Model):
    logistics_num = models.CharField(max_length=50)
    order_num = models.CharField(max_length=255, primary_key=True)
    logistics_company_code = models.CharField(max_length=255)
    logistics_company = models.CharField(max_length=50)
    logistice_cost = models.DecimalField(max_digits=10, decimal_places=2)
    consignee_user_name = models.CharField(max_length=255)
    consignee_phone = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    detail_addr = models.CharField(max_length=255)
    logistics_status = models.SlugField(default='0')
    delivery_time = models.DateTimeField()
    received_time = models.DateTimeField()
    # goods_logistics = models.OneToOneField(TakeOrder, on_delete=models.CASCADE)


    class Meta:
        db_table = 'take_order_logistics'
        verbose_name = '提货订单_快递表'
        verbose_name_plural = verbose_name

# 代言商品表
class RepreSent(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    foreign_key = models.CharField(max_length=255)
    represent_id = models.CharField(max_length=255)
    goods_id = models.CharField(max_length=255)
    represent_time = models.DateTimeField()
    operation_result = models.SlugField(default='0')
    amount = models.SlugField(default='0')
    user_id = models.CharField(max_length=50)
    surplus = models.SlugField(default='0')
    type = models.SlugField(default='3')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    import_people = models.SlugField(default='0')

    class Meta:
        db_table = 'represent'
        verbose_name = '代言商品表'
        verbose_name_plural = verbose_name


# 商品信息表
class TransferRecord(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    userAddr = models.CharField(max_length=255)
    goodsAddr = models.CharField(max_length=255)
    amount = models.SlugField(default='0')
    remainingNum = models.SlugField(default='0')
    userAmount = models.SlugField(default='0')
    receivedNum = models.SlugField(default='1')
    refundedNum = models.SlugField(default='0')
    cardType = models.SlugField(default='0')
    createdAt = models.DateTimeField()


    class Meta:
        db_table = 'transfer_record'
        verbose_name = '商品转赠表'
        verbose_name_plural = verbose_name

# 用户openid来源
class Jlduser_Source(models.Model):
    user_union_id = models.CharField(max_length=255, primary_key=True)
    user_open_id = models.CharField(max_length=255)
    openid_source = models.SlugField()

    class Meta:
        db_table = 'jld_user_source'
        verbose_name = '用户openid来源'
        verbose_name_plural = verbose_name

# 商家活动表
class OrgActivity(models.Model):
    id = models.CharField(max_length=255)
    activityId = models.CharField(max_length=255, primary_key=True)
    createdAt = models.DateTimeField()
    goodsAddr = models.CharField(max_length=255)
    startRob = models.DateTimeField()
    stopRob = models.DateTimeField()
    robNum = models.SlugField(default='0')
    debrisNum = models.SlugField(default='0')
    times = models.SlugField(default='0')
    participants = models.SlugField(default='0')
    isShow = models.SlugField(default='1')
    remainingRob = models.SlugField(default='0')
    orgAddr = models.CharField(max_length=255)
    returnRobNum = models.SlugField(default='0')

    class Meta:
        db_table = 'org_activity'
        verbose_name = '商家活动表'
        verbose_name_plural = verbose_name


# 代言券转增记录
class Reviewrecord(models.Model):
    from_user = models.CharField(max_length=255, primary_key=True)
    to_user = models.CharField(max_length=255)
    amount = models.SlugField(default='0')
    created_time = models.DateTimeField()
    represent_id = models.CharField(max_length=255)
    source = models.SlugField(default='1')
    is_delete = models.SlugField(default='0')

    class Meta:
        db_table = 'reviewrecord'
        verbose_name = '代言券转增记录'
        verbose_name_plural = verbose_name

# 用户openid来源
class Rob_Help (models.Model):
    activity = models.CharField(max_length=255, primary_key=True)
    goodsAddr = models.CharField(max_length=255)
    toUserAddr = models.CharField(max_length=255)

    class Meta:
        db_table = 'rob_help '
        verbose_name = '好友助力表'
        verbose_name_plural = verbose_name

# 活动用户表
class Activity_User  (models.Model):
    activityId = models.CharField(max_length=255, primary_key=True)
    goodsAddr = models.CharField(max_length=255)
    isRob = models.CharField(max_length=255)

    class Meta:
        db_table = 'rob_help '
        verbose_name = '好友助力表'
        verbose_name_plural = verbose_name



# 用户资产表
class Endorsementuser(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    unionid = models.CharField(max_length=64)
    wx_nick_name = models.CharField(max_length=64)
    cash_withdrawal = models.SlugField(default='0')
    frozen = models.SlugField(default='0')
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=64)
    sex = models.SlugField(default='1')
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'endorsement_user'
        verbose_name = '用户资产表'
        verbose_name_plural = verbose_name

