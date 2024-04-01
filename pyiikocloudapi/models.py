from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any


class IdNameModel(BaseModel):
    id: str
    name: str

    def __str__(self):
        return self.name


class BaseResponseModel(BaseModel):
    correlation_id: Optional[str] = Field(alias='correlationId')


class ErrorModel(BaseResponseModel):
    error_description: Optional[str] = Field(alias='errorDescription')
    error: Optional[str]


class CustomErrorModel(ErrorModel):
    status_code: Optional[str]


class OrganizationModel(IdNameModel):
    class ResponseTypeEnum(str, Enum):
        simple = "Simple"
        extended = "Extended"

    class OAddressFormatTypeEnum(str, Enum):
        legacy = "Legacy"
        city = "City"
        international = "International"
        int_no_postcode = "IntNoPostcode"

    country: Optional[str]
    restaurant_address: Optional[str] = Field(alias="restaurantAddress")
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    use_uae_addressing_system: Optional[bool] = Field(alias="useUaeAddressingSystem")
    version: Optional[str]
    currency_iso_name: Optional[str] = Field(alias="currencyIsoName")
    currency_minimum_denomination: Optional[Decimal] = Field(alias="currencyMinimumDenomination")
    country_phone_code: Optional[str] = Field(alias="countryPhoneCode")
    marketing_source_required_in_delivery: Optional[bool] = Field(alias="marketingSourceRequiredInDelivery")
    default_delivery_city_id: Optional[str] = Field(alias="defaultDeliveryCityId")
    delivery_city_ids: Optional[List[str]] = Field(alias="deliveryCityIds")
    delivery_service_type: Optional[str] = Field(alias="deliveryServiceType")
    default_call_center_payment_type_id: Optional[str] = Field(alias="defaultCallCenterPaymentTypeId")
    order_item_comment_enabled: Optional[bool] = Field(alias="orderItemCommentEnabled")
    inn: Optional[str]
    addressFormatType: Optional[OAddressFormatTypeEnum] = Field(alias="addressFormatType")
    is_confirmation_enabled: Optional[bool] = Field(alias="isConfirmationEnabled")
    confirm_allowed_interval_in_minutes: Optional[int] = Field(alias="confirmAllowedIntervalInMinutes")
    response_type: ResponseTypeEnum = Field(alias="responseType")

    def __str__(self):
        return self.name

class OrganizationExtendedModel(IdNameModel):
    class ResponseTypeEnum(str, Enum):
        simple = "Simple"
        extended = "Extended"

    class OAddressFormatTypeEnum(str, Enum):
        legacy = "Legacy"
        city = "City"
        international = "International"
        int_no_postcode = "IntNoPostcode"

    country: Optional[str]
    restaurant_address: Optional[str] = Field(alias="restaurantAddress")
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    use_uae_addressing_system: Optional[bool] = Field(alias="useUaeAddressingSystem")
    version: Optional[str]
    currency_iso_name: Optional[str] = Field(alias="currencyIsoName")
    currency_minimum_denomination: Optional[Decimal] = Field(alias="currencyMinimumDenomination")
    country_phone_code: Optional[str] = Field(alias="countryPhoneCode")
    marketing_source_required_in_delivery: Optional[bool] = Field(alias="marketingSourceRequiredInDelivery")
    default_delivery_city_id: Optional[str] = Field(alias="defaultDeliveryCityId")
    delivery_city_ids: Optional[List[str]] = Field(alias="deliveryCityIds")
    delivery_service_type: Optional[str] = Field(alias="deliveryServiceType")
    default_call_center_payment_type_id: Optional[str] = Field(alias="defaultCallCenterPaymentTypeId")
    order_item_comment_enabled: Optional[bool] = Field(alias="orderItemCommentEnabled")
    inn: Optional[str]
    addressFormatType: Optional[OAddressFormatTypeEnum] = Field(alias="addressFormatType")
    is_confirmation_enabled: Optional[bool] = Field(alias="isConfirmationEnabled")
    confirm_allowed_interval_in_minutes: Optional[int] = Field(alias="confirmAllowedIntervalInMinutes")
    response_type: ResponseTypeEnum = Field(alias="responseType")

    def __str__(self):
        return self.name



class BaseOrganizationsModel(BaseResponseModel):
    organizations: List[OrganizationModel]


    def __list_id__(self):
        return [org.id for org in self.organizations]


class EmployeeItemModel(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias='firstName')
    middle_name: Optional[str] = Field(alias='middleName')
    last_name: Optional[str] = Field(alias='lastName')
    display_name: str = Field(alias='displayName')
    code: str
    is_deleted: bool = Field(alias='isDeleted')


class EmployeesModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    items: Optional[List[EmployeeItemModel]]


class CouriersModel(BaseResponseModel):
    employees: List[EmployeesModel]

    def get_by_employee_code(self, employee_code: str):
        return next(x for i in self.employees for x in i.items if x.code == employee_code)

    def get_by_employee_id(self, employee_id: str):
        return next(x for i in self.employees for x in i.items if x.id == employee_id)


class CustomerModel(BaseModel):
    id: str
    name: str
    surname: Optional[str]
    comment: Optional[str]
    gender: str
    inBlacklist: bool
    blacklistReason: Optional[str]
    birthdate: Optional[str]


class CauseModel(BaseModel):
    id: str
    name: str


class CancelInfoModel(BaseModel):
    whenCancelled: str
    cause: CauseModel
    comment: Optional[str]


class EmployeeModel(BaseModel):
    id: str
    name: str
    phone: Optional[str]


class CourierInfoModel(BaseModel):
    courier: EmployeeModel
    is_courier_selected_manually: bool = Field(alias="isCourierSelectedManually")


class ProblemOrderModel(BaseModel):
    has_problem: bool = Field(alias="hasProblem")
    description: Optional[str]


class MarketingSourceOrderModel(BaseModel):
    id: str
    name: str


class ExternalCourierServiceOrderModel(BaseModel):
    id: str
    name: str


class ConceptionOrderModel(BaseModel):
    id: str
    name: str
    code: str


class GuestsInfoOrderModel(BaseModel):
    count: int
    split_between_persons: bool = Field(alias="splitBetweenPersons")


class CombosItemOrderModel(BaseModel):
    id: str
    name: str
    amount: int
    price: float
    source_id: str = Field(alias="sourceId")


class PIOPaymentTypeModel(BaseModel):
    id: str
    name: str
    kind: str


class PaymentItemOrderModel(BaseModel):
    payment_type: PIOPaymentTypeModel = Field(alias="paymentType")
    sum: float
    is_preliminary: bool = Field(alias="isPreliminary")
    is_external: bool = Field(alias="isExternal")
    is_processed_externally: bool = Field(alias="isProcessedExternally")
    is_fiscalized_externally: Optional[bool] = Field(alias="isFiscalizedExternally")


class TipsTypeModel(BaseModel):
    id: str
    name: str


class TipsItemOrderModel(BaseModel):
    tips_type: TipsTypeModel = Field(alias="tipsType")
    payment_type: PIOPaymentTypeModel = Field(alias="paymentType")
    sum: float
    is_preliminary: bool = Field(alias="isPreliminary")
    is_external: bool = Field(alias="isExternal")
    is_processed_externally: bool = Field(alias="isProcessedExternally")
    is_fiscalized_externally: Optional[bool] = Field(alias="isFiscalizedExternally")


class DiscountTypeModel(BaseModel):
    id: str
    name: str


class OrderItemComboInformationModel(BaseModel):
    combo_id: str = Field(alias="comboId")
    combo_source_id: str = Field(alias="comboSourceId")
    group_id: str = Field(alias="groupId")


class DiscountsItemOrderModel(BaseModel):
    discount_type: DiscountTypeModel = Field(alias="discountType")
    sum: float
    selective_positions: Optional[List[str]] = Field(alias="selectivePositions")


class OrderItemDeletionMethodModel(BaseModel):
    id: str
    comment: Optional[str]
    removal_type: IdNameModel


class OrderItemDeletedModel(BaseModel):
    deletion_method: OrderItemDeletionMethodModel


class CDOrderTypeModel(BaseModel):
    id: str
    name: str
    order_service_type: str = Field(alias="orderServiceType")


class MOrderProductItemModel(BaseModel):
    product: IdNameModel = Field(alias="product")
    amount: float
    amount_independent_of_parent_amount: bool = Field(alias="amountIndependentOfParentAmount")
    product_group: IdNameModel = Field(alias="productGroup")
    price: float
    price_predefined: bool = Field(alias="pricePredefined")
    result_sum: Optional[float]
    deleted: Optional[OrderItemDeletedModel]
    position_id: Optional[str] = Field(alias="positionId")
    default_amount: Optional[int] = Field(alias="defaultAmount")
    hide_if_default_amount: Optional[bool] = Field(alias="hideIfDefaultAmount")
    tax_percent: Optional[float] = Field(alias="taxPercent")


class OrderProductItemModel(BaseModel):
    product: IdNameModel = Field(alias="product")
    modifiers: Optional[List[MOrderProductItemModel]]
    price: Optional[float]
    cost: float
    price_predefined: bool = Field(alias="pricePredefined")
    position_id: Optional[str] = Field(alias="positionId")
    tax_percent: Optional[float] = Field(alias="taxPercent")
    type: str
    status: str
    deleted: Optional[OrderItemDeletedModel]
    amount: float
    comment: Optional[str]
    when_printed: Optional[str] = Field(alias="whenPrinted")
    size: Optional[IdNameModel]
    combo_information: Optional[OrderItemComboInformationModel] = Field(alias="comboInformation")


class CreatedDeliveryOrderModel(BaseModel):
    parent_delivery_id: Optional[str] = Field(alias="parentDeliveryId")
    customer: CustomerModel
    phone: str
    # TODO(Kebrick): дописать модель DeliveryPointModel для ключа delivery_point
    delivery_point: Optional[dict] = Field(alias="deliveryPoint")
    status: str
    cancel_info: Optional[CancelInfoModel] = Field(alias="cancelInfo")
    courier_info: Optional[CourierInfoModel] = Field(alias="courierInfo")
    complete_before: str = Field(alias="completeBefore")
    when_created: str = Field(alias="whenCreated")
    when_confirmed: Optional[str] = Field(alias="whenConfirmed")
    when_printed: Optional[str] = Field(alias="whenPrinted")
    when_sended: Optional[str] = Field(alias="whenSended")
    when_delivered: Optional[str] = Field(alias="whenDelivered")
    comment: Optional[str]
    problem: Optional[ProblemOrderModel]
    operator: Optional[EmployeeModel]
    marketing_source: Optional[MarketingSourceOrderModel] = Field(alias="marketingSource")
    delivery_duration: Optional[int] = Field(alias="deliveryDuration")
    index_in_courier_route: Optional[int] = Field(alias="indexInCourierRoute")
    cooking_start_time: str = Field(alias="cookingStartTime")
    is_deleted: bool = Field(alias="isDeleted")
    when_received_by_api: Optional[str] = Field(alias="whenReceivedByApi")
    when_received_from_front: Optional[str] = Field(alias="whenReceivedFromFront")
    moved_from_delivery_id: Optional[str] = Field(alias="movedFromDeliveryId")
    moved_from_terminal_group_id: Optional[str] = Field(alias="movedFromTerminalGroupId")
    moved_from_organization_id: Optional[str] = Field(alias="movedFromOrganizationId")
    external_courier_service: Optional[ExternalCourierServiceOrderModel] = Field(alias="externalCourierService")
    sum: float
    number: int
    source_key: Optional[str] = Field(alias="sourceKey")
    when_bill_printed: Optional[str] = Field(alias="whenBillPrinted")
    when_closed: Optional[str] = Field(alias="whenClosed")
    conception: Optional[ConceptionOrderModel]
    guests_info: GuestsInfoOrderModel = Field(alias="guestsInfo")
    # TODO(Kebrick): дописать модель ItemsOrderModel для ключа items
    items: List[OrderProductItemModel]
    combos: Optional[List[CombosItemOrderModel]]
    payments: Optional[List[PaymentItemOrderModel]]
    tips: Optional[List[TipsItemOrderModel]]
    discounts: Optional[List[DiscountsItemOrderModel]]
    order_type: Optional[CDOrderTypeModel] = Field(alias="orderType")
    terminal_group_id: str = Field(alias="terminalGroupId")
    processed_payments_sum: Optional[int] = Field(alias="processedPaymentsSum")


class ErrorInfoModel(BaseModel):
    # "code": "Common",
    # "message": "string",
    # "description": "string",
    # "additionalData": null
    code: str
    message: Optional[str]
    description: Optional[str]
    additional_data: Optional[Union[str, list]] = Field(alias="additionalData")


class ByOrderItemModel(BaseModel):
    id: str
    external_number: Optional[str] = Field(alias='externalNumber')
    organization_id: str = Field(alias='organizationId')
    timestamp: int
    creation_status: Optional[str] = Field(alias='creationStatus')
    error_info: Optional[ErrorInfoModel] = Field(alias='errorInfo')
    order: Optional[CreatedDeliveryOrderModel]

    def get_by_courier_id(self, courier_id: str):
        # return next(i for i in self.orders if i.order.courier_info is not None and str(i.order.courier_info.courier.id) == courier_id)

        return self if self.order.courier_info is not None and self.order.courier_info.courier.id == courier_id else None


class ByIdModel(BaseResponseModel):
    orders: Optional[List[ByOrderItemModel]]


class OrdersByOrganizationsModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    orders: Optional[List[ByOrderItemModel]]

    def get_by_courier_name(self, courier_name: str):
        return next(i for i in self.orders if
                    i.order.courier_info is not None and str(i.order.courier_info.courier.name) == courier_name)

    def get_by_courier_id(self, courier_id: str):
        return next(i for i in self.orders if
                    i.order.courier_info is not None and i.order.courier_info.courier.id == courier_id)

    # def get_by_courier_id_v2(self, courier_id: str):
    #     for i in self.orders:
    #         out = i.get_by_courier_id(courier_id)
    #         if out is not None:
    #             return out


class ByDeliveryDateAndStatusModel(BaseResponseModel):
    max_revision: int = Field(alias="maxRevision")
    orders_by_organizations: Optional[List[OrdersByOrganizationsModel]] = Field(alias="ordersByOrganizations")


class ByDeliveryDateAndSourceKeyAndFilter(ByDeliveryDateAndStatusModel):
    pass


class RegionsItemModel(BaseModel):
    id: str
    name: str
    external_revision: Optional[int] = Field(alias="externalRevision")
    is_deleted: bool = Field(alias='isDeleted')


class RegionsModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    items: Optional[List[RegionsItemModel]]


class BaseRegionsModel(BaseResponseModel):
    regions: Optional[List[RegionsModel]]


class CitiesItemModel(BaseModel):
    id: str
    name: str
    external_revision: Optional[int] = Field(alias="externalRevision")
    is_deleted: bool = Field(alias='isDeleted')
    classifier_id: Optional[str] = Field(alias="classifierId")
    additional_info: Optional[str] = Field(alias="additionalInfo")


class CitiesModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    items: Optional[List[CitiesItemModel]]


class BaseCitiesModel(BaseResponseModel):
    cities: Optional[List[CitiesModel]]


class StreetsItemModel(BaseModel):
    id: str
    name: str
    external_revision: Optional[int] = Field(alias="externalRevision")
    classifier_id: Optional[str] = Field(alias="classifierId")
    is_deleted: bool = Field(alias='isDeleted')


# class StreetsModel(BaseModel):
#     correlation_id: str = Field(alias='correlationId')
#     items: Optional[List[RegionsItemModel]]


class BaseStreetByCityModel(BaseResponseModel):
    streets: Optional[List[StreetsItemModel]]


class TerminalGroupItemModel(BaseModel):
    id: str
    name: str
    organization_id: str = Field(alias="organizationId")
    address: Optional[str]


class TerminalGroupsModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    items: Optional[List[TerminalGroupItemModel]]


class BaseTerminalGroupsModel(BaseResponseModel):
    terminal_groups: Optional[List[TerminalGroupsModel]] = Field(alias="terminalGroups")


class TGIsAliveItemModel(BaseModel):
    isAlive: bool = Field(alias="isAlive")
    terminal_group_id: str = Field(alias="terminalGroupId")
    organization_id: str = Field(alias='organizationId')


class BaseTGIsAliveyModel(BaseResponseModel):
    is_alive_status: Optional[List[TGIsAliveItemModel]] = Field(alias="isAliveStatus")


# class COrderCustomerModel(BaseModel):
#     id: Optional[str]
#     name: Optional[str]
#     surname: Optional[str]
#     comment: Optional[str]
#     birthdate: Optional[str]
#     email: Optional[str]
#     should_receive_order_status_notifications: Optional[bool] = Field(alias="shouldReceiveOrderStatusNotifications")
#     gender: Optional[str]
#
#
# class COrderGuestsModel(BaseModel):
#     count: int
#
#
# class COrderComboModel(BaseModel):
#     id: str
#     name: str
#     amount: float
#     price: float
#     source_id: str = Field(alias="sourceId")
#     program_id: Optional[str] = Field(alias="programId")
#
#
# class COrderPaymentAdditionalDataModel(BaseModel):
#     credential: str
#     search_scope: str = Field(alias="searchScope", )
#     type: str
#
#
# class COrderPaymentModel(BaseModel):
#     payment_type_kind: str = Field(alias="paymentTypeKind")
#     sum: float
#     payment_type_id: str = Field(alias="paymentTypeId")
#     is_processed_externally: Optional[bool] = Field(alias="isProcessedExternally")
#     payment_additional_data: Optional[COrderPaymentAdditionalDataModel] = Field(alias="paymentAdditionalData")
#     is_fiscalized_externally: Optional[bool] = Field(alias="isFiscalizedExternally")
#
#
# class COrderTipsItemModel(BaseModel):
#     payment_type_kind: str = Field(alias="paymentTypeKind")
#     payment_type_id: str = Field(alias="paymentTypeId")
#     sum: float
#     tips_type_id: Optional[str] = Field(alias="tipsTypeId")
#     is_processed_externally: Optional[bool] = Field(alias="isProcessedExternally")
#     payment_additional_data: Optional[COrderPaymentAdditionalDataModel] = Field(alias="paymentAdditionalData")
#     is_fiscalized_externally: Optional[bool] = Field(alias="isFiscalizedExternally")
#
#
# class COrderCardModel(BaseModel):
#     track: str
#
#
# class COrderDiscountsModel(BaseModel):
#     discount_type_id: str = Field(alias="discountTypeId")
#     sum: Optional[float]
#     selective_positions: Optional[List[str]] = Field(alias="selectivePositions")
#     type: str
#
#
# class COrderDiscountsInfoModel(BaseModel):
#     card: Optional[COrderCardModel]
#     discounts: Optional[List[COrderDiscountsModel]]
#
#
# class COrderIikoCard5InfoModel(BaseModel):
#     coupon: Optional[str]
#     applicable_manual_conditions: Optional[List[str]] = Field(alias="applicableManualConditions")
#
#
# class COrderModel(BaseModel):
#     id: Optional[str]
#     external_number: Optional[str] = Field(alias='externalNumber')
#     table_ids: Optional[List[str]]
#     customer: Optional[CustomerModel]
#     phone: Optional[str]
#     guests: Optional[COrderGuestsModel]
#     tab_name: Optional[str] = Field(alias="tabName")
#     items: List[COrderItemsModel]
#     combos: Optional[List[COrderComboModel]]
#     payments: Optional[List[COrderPaymentModel]]
#     tips: Optional[List[COrderTipsItemModel]]
#     source_key: Optional[str] = Field(alias="sourceKey")
#     discounts_info: Optional[COrderDiscountsInfoModel] = Field(alias="discountsInfo")
#     iiko_card5_info: Optional[COrderIikoCard5InfoModel] = Field(alias="iikoCard5Info")
#     order_type_id: Optional[str] = Field("orderTypeId")
#
#
# class COrderSettings(BaseModel):
#     transport_to_front_timeout: int = Field(alias="transportToFrontTimeout", default=0)
#
#
# class BaseCOrderModel(BaseModel):
#     organization_id: str = Field(alias="organizationId")
#     terminal_group_id: Optional[str] = Field(alias="terminalGroupId")
#     order: COrderModel
#     createOrderSettings: Optional[COrderSettings]


class OrderDetailWaiterModel(IdNameModel):
    phone: Optional[str]


class OrderItemCreatedModel(BaseModel):
    product: IdNameModel
    modifiers: Optional[List[dict]]
    price: float
    cost: float
    price_predefined: bool = Field(alias="pricePredefined")
    position_id: Optional[str] = Field(alias="positionId")
    tax_percent: Optional[float] = Field(alias="taxPercent")
    type: str
    status: str
    deleted: Optional[OrderItemDeletedModel]
    amount: float
    comment: Optional[str]
    when_printed: Optional[str]
    size: Optional[IdNameModel]
    combo_information: Optional[OrderItemComboInformationModel] = Field(alias="comboInformation")


class CreateOrderDetailModel(CreatedDeliveryOrderModel):
    table_ids: Optional[List[str]]
    waiter: Optional[OrderDetailWaiterModel]
    tab_name: Optional[str] = Field(alias="tabName")

class COICreationStatusModel(str, Enum):
    success = "Success"
    in_progress = "InProgress"
    error = "Error"

class CreatedOrderInfoModel(BaseModel):
    id: str
    external_number: Optional[str] = Field(alias='externalNumber')
    organization_id: str = Field(alias='organizationId')
    timestamp: int
    creation_status: Optional[COICreationStatusModel] = Field(alias='creationStatus')
    error_info: Optional[ErrorInfoModel] = Field(alias="errorInfo")
    order: CreateOrderDetailModel


class CreateDeliveryOrderInfoModel(CreatedOrderInfoModel):
    order: Optional[CreatedDeliveryOrderModel]


class BaseCreatedOrderInfoModel(BaseResponseModel):
    order_info: CreatedOrderInfoModel = Field(alias="orderInfo")


class BaseCreatedDeliveryOrderInfoModel(BaseResponseModel):
    order_info: CreateDeliveryOrderInfoModel = Field(alias="orderInfo")


class NomenclatureGroupModel(BaseModel):
    """
    imageLinks - Links to images.
    parentGroup	- Parent group.
    order - Group's order (priority) in menu.
    isIncludedInMenu - On-the-menu attribute.
    isGroupModifier - Is group modifier attribute.true - group modifier. false - external menu group.
    id - ID.
    code - SKU.
    name - Name.
    description	- Description.
    additionalInfo - Additional information.
    tags - Tags.
    isDeleted - Is-Deleted attribute.
    seoDescription - SEO description for client.
    seoText	- SEO text for robots.
    seoKeywords	- SEO key words.
    seoTitle - SEO header.
    """
    image_links: List[str] = Field(alias="imageLinks")
    parent_group: Optional[str] = Field(alias="parentGroup")
    order: int
    is_included_in_menu: bool = Field(alias="isIncludedInMenu")
    is_group_modifier: bool = Field(alias="isGroupModifier")
    id: str
    code: Optional[str]
    name: str
    description: Optional[str]
    additional_info: Optional[str] = Field(alias="additionalInfo")
    tags: Optional[List[str]]
    is_deleted: Optional[bool] = Field(alias="isDeleted")
    seo_description: Optional[str] = Field(alias="seoDescription")
    seo_text: Optional[str] = Field(alias="seoText")
    seo_keywords: Optional[str] = Field(alias="seoKeywords")
    set_title: Optional[str] = Field(alias="seoTitle")

    def __str__(self):
        return self.name


class NProductCategoriesModel(BaseModel):
    id: str
    name: str
    is_deleted: bool = Field(alias="isDeleted")

    def __str__(self):
        return self.name


class NSizeModel(BaseModel):
    id: str
    name: str
    priority: Optional[int]
    is_default: Optional[bool] = Field(alias="isDefault")

    def __str__(self):
        return self.name


class NPSPPriceModel(BaseModel):
    current_price: float = Field(alias="currentPrice")
    is_included_in_menu: bool = Field(alias="isIncludedInMenu")
    next_price: Optional[float] = Field(alias="nextPrice")
    next_included_in_menu: bool = Field(alias="nextIncludedInMenu")
    next_date_price: Optional[str] = Field(alias="nextDatePrice")

    def __str__(self):
        return self.current_price


class NPSizePriceModel(BaseModel):
    size_id: Optional[str]
    price: NPSPPriceModel


class NPModifierModel(BaseModel):
    id: str
    default_amount: Optional[int] = Field(alias="defaultAmount")
    min_amount: int = Field(alias="minAmount")
    max_amount: int = Field(alias="maxAmount")
    required: Optional[bool]
    hide_if_default_amount: Optional[bool] = Field(alias='hideIfDefaultAmount')
    splittable: Optional[bool]
    free_of_charge_amount: Optional[int] = Field(alias="freeOfChargeAmount")

    def __str__(self):
        return self.id


class NPGroupModifierModel(BaseModel):
    id: str
    min_amount: int = Field(alias="minAmount")
    max_amount: int = Field(alias="maxAmount")
    required: bool
    child_modifiers_have_min_max_restrictions: Optional[bool] = Field(alias='childModifiersHaveMinMaxRestrictions')
    child_modifiers: List[NPModifierModel] = Field(alias='childModifiers')
    hide_if_default_amount: Optional[bool] = Field(alias='hideIfDefaultAmount')
    default_amount: Optional[int] = Field(alias="defaultAmount")
    splittable: Optional[bool]
    free_of_charge_amount: Optional[int] = Field(alias="freeOfChargeAmount")

    def __str__(self):
        return self.id


class NProductModel(BaseModel):
    fat_amount: Optional[float] = Field(alias="fatAmount")
    proteins_amount: Optional[float] = Field(alias="proteinsAmount")
    carbohydrates_amount: Optional[float] = Field(alias="energyAmount")
    energy_amount: Optional[float] = Field(alias="carbohydratesAmount")
    fat_full_amount: Optional[float] = Field(alias="fatFullAmount")
    proteins_full_amount: Optional[float] = Field(alias="proteinsFullAmount")
    carbohydrates_full_amount: Optional[float] = Field(alias="carbohydratesFullAmount")
    energy_full_amount: Optional[float] = Field(alias="energyFullAmount")
    weight: Optional[float]
    group_id: Optional[str] = Field(alias="groupId")
    product_category_id: Optional[str] = Field(alias="productCategoryId")
    type: Optional[str]
    order_item_type: str = Field(alias="orderItemType")
    modifier_schema_id: Optional[str] = Field(alias="modifierSchemaId")
    modifier_schema_name: Optional[str] = Field(alias="modifierSchemaName")
    splittable: bool
    measure_unit: str = Field(alias="measureUnit")
    size_prices: List[NPSizePriceModel] = Field(alias="sizePrices")
    modifiers: List[NPModifierModel]
    group_modifiers: List[Optional[NPGroupModifierModel]] = Field(alias='groupModifiers')
    image_links: List[str] = Field(alias="imageLinks")
    do_not_print_in_cheque: bool = Field(alias='doNotPrintInCheque')
    parent_group: Optional[str] = Field(alias='parentGroup')
    order: int
    full_name_english: Optional[str] = Field(alias='fullNameEnglish')
    use_balance_for_sell: bool = Field(alias='useBalanceForSell')
    can_set_open_price: bool = Field(alias="canSetOpenPrice")
    id: str
    code: Optional[str]
    name: str
    description: Optional[str]
    additional_info: Optional[str] = Field(alias='additionalInfo')
    tags: Optional[List[str]]
    is_deleted: Optional[bool] = Field(alias="isDeleted")
    seo_description: Optional[str] = Field(alias="seoDescription")
    seo_text: Optional[str] = Field(alias="seoText")
    seo_keywords: Optional[str] = Field(alias="seoKeywords")
    set_title: Optional[str] = Field(alias="seoTitle")

    def __str__(self):
        return self.name


class BaseNomenclatureModel(BaseResponseModel):
    groups: List[NomenclatureGroupModel]
    product_categories: List[NProductCategoriesModel] = Field(alias="productCategories")
    products: List[NProductModel]
    sizes: List[NSizeModel]
    revision: int

    def __str__(self):
        return str(self.revision)


class BaseMenuModel(BaseResponseModel):
    external_menus: Optional[List[IdNameModel]] = Field(alias="externalMenus")
    price_categories: Optional[List[IdNameModel]] = Field(alias="priceCategories")


class ICIAllergenGroupModel(IdNameModel):
    code: str


class MBIdICTaxCategoryModel(IdNameModel):
    percentage: float


class MBIdICISPriceModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    price: float


class MBIdICISIMGRestrictionModel(BaseModel):
    min_quantity: int
    max_quantity: int
    free_quantity: int
    by_default: int


class MBIdICISIMGItemModel(BaseModel):
    prices: List[MBIdICISPriceModel]
    sku: str
    name: str
    description: str
    button_image: str = Field(alias='buttonImage')
    restrictions: MBIdICISIMGRestrictionModel
    allergen_groups: List[ICIAllergenGroupModel] = Field(alias='allergenGroups')
    nutrition_per_hundred_grams: dict = Field(alias='nutritionPerHundredGrams')
    portion_weight_grams: float = Field(alias='portionWeightGrams')
    tags: List[IdNameModel]
    item_id: str = Field(alias='itemId')


class MBIdICISItemModifierGroupModel(BaseModel):
    items: List[MBIdICISIMGItemModel]
    name: str
    description: str
    restrictions: MBIdICISIMGRestrictionModel
    can_be_divided: bool = Field(alias='canBeDivided')
    item_group_id: str = Field(alias='itemGroupId')
    child_modifiers_have_min_max_restrictions: bool = Field(alias="childModifiersHaveMinMaxRestrictions")
    sku: str


class MBIdICItemSizeModel(BaseModel):
    prices: MBIdICISPriceModel
    item_modifier_groups: List[MBIdICISItemModifierGroupModel] = Field(alias='itemModifierGroups')
    sku: str
    size_code: str = Field(alias='sizeCode')
    size_name: str = Field(aliad='sizeName')
    is_default: Optional[bool] = Field(alias="isDefault")
    portion_weight_grams: float = Field(alias='portionWeightGrams')
    size_id: str = Field(alias='sizeId')
    nutrition_per_hundred_grams: dict = Field(alias='nutritionPerHundredGrams')
    button_image_url: str = Field(alias="buttonImageUrl")
    button_image_cropped_url: str = Field(alias="buttonImageCroppedUrl")


class MBIdICItemModel(BaseModel):
    sku: str
    name: str
    description: str
    allergen_groups: List[ICIAllergenGroupModel] = Field(alias='allergenGroups')
    item_id: str = Field(alias='itemId')
    modofier_schema_id: str = Field(alias='modofierSchemaId')
    tax_category: MBIdICTaxCategoryModel
    order_item_type: str
    item_sizes: List[MBIdICItemSizeModel]

    def __str__(self):
        return self.name


class MBIdItemCategoryModel(IdNameModel):
    description: str
    button_image_url: str = Field(alias="buttonImageUrl")
    header_image_url: str = Field(alias="headerImageUrl")
    items: List[MBIdICItemModel]


class BaseMenuByIdModel(IdNameModel):
    description: str
    item_categories: List[MBIdItemCategoryModel] = Field(alias="itemCategories")


# Cancel Causes
class CCItemModel(IdNameModel):
    is_deleted: bool = Field(alias='isDeleted')


class BaseCancelCausesModel(BaseResponseModel):
    cancel_causes: List[CCItemModel] = Field(alias='cancelCauses')


# OrderTypes
class ORTItemModel(IdNameModel):
    order_service_type: str = Field(alias='orderServiceType')
    is_deleted: bool = Field(alias='isDeleted')
    external_revision: Optional[int] = Field(alias="externalRevision")


class OrderTypeModel(BaseModel):
    organization_id: str = Field(alias="organizationId")
    items: List[ORTItemModel]


class BaseOrderTypesModel(BaseResponseModel):
    order_types: List[OrderTypeModel] = Field(alias='orderTypes')


# Discounts
class DIProductCategoryDiscountsModel(BaseModel):
    category_id: str = Field(alias="categoryId")
    category_name: Optional[str] = Field(alias='categoryName')
    percent: float


class DItemModel(IdNameModel):
    percent: float
    is_categorised_discount: bool = Field(alias='isCategorisedDiscount')
    product_category_discounts: List[DIProductCategoryDiscountsModel] = Field(alias='productCategoryDiscounts')
    comment: Optional[str]
    can_be_applied_selectively: str = Field(alias='canBeAppliedSelectively')
    min_order_sum: Optional[float] = Field(aliad='minOrderSum')
    mode: str
    sum: float
    can_apply_by_card_number: bool = Field(alias='canApplyByCardNumber')
    is_manual: bool = Field(alias='isManual')
    is_card: bool = Field(alias='isCard')
    is_automatic: bool = Field(alias='isAutomatic')
    is_deleted: bool = Field(alias='isDeleted')


class DiscountModel(BaseModel):
    organization_id: str
    items: List[DItemModel]


class BaseDiscountsModel(BaseResponseModel):
    discounts: List[DiscountModel]

class CouponInfo(BaseModel):
    id: str
    number: Optional[str]
    seriesName: Optional[str]
    seriesId: Optional[str]
    whenActivated: Optional[str]
    isDeleted: Optional[str]

class SeriesWithNotActivatedCoupon(BaseModel):
    coupons: List[CouponInfo] = Field(alias="seriesWithNotActivatedCoupons")

class BaseCouponInfo(BaseModel):
    coupons: List[CouponInfo] = Field(alias="couponInfo")


# Payment Types
class PaymentTypeModel(IdNameModel):
    code: Optional[str]
    comment: Optional[str]
    combinable: bool
    external_revision: Optional[int] = Field(alias="externalRevision")
    applicable_marketing_campaigns: List[str] = Field(alias="applicableMarketingCampaigns")
    is_deleted: bool = Field(alias='isDeleted')
    print_cheque: bool = Field(alias='printCheque')
    payment_processing_type: Optional[str] = Field(alias='paymentProcessingType')
    payment_type_kind: Optional[str] = Field(alias='paymentTypeKind')
    terminal_groups: List[TerminalGroupItemModel] = Field(alias='terminalGroups')


class BasePaymentTypesModel(BaseResponseModel):
    payment_types: List[PaymentTypeModel] = Field(alias='paymentTypes')

    def __list_id__(self):
        return [pt.id for pt in self.payment_types]


# Removal Types
class RemovalTypeModel(IdNameModel):
    comment: Optional[str]
    can_writeoff_to_cafe: bool = Field(alias="canWriteoffToCafe")
    can_writeoff_to_waiter: bool = Field(alias="canWriteoffToWaiter")
    can_writeoff_to_user: bool = Field(alias="canWriteoffToUser")
    reason_required: bool = Field(alias="reasonRequired")
    manual: bool
    is_deleted: bool = Field(alias='isDeleted')


class BaseRemovalTypesModel(BaseResponseModel):
    removal_types: List[RemovalTypeModel] = Field(alias="removalTypes")


# Получите подсказки для группы api-logins rms.
class TipTypeModel(IdNameModel):
    organization_ids: List[str] = Field(alias="organizationIds")
    order_service_types: List[str] = Field(alias="orderServiceTypes")
    payment_types_ids: List[str] = Field(alias="paymentTypesIds")


class BaseTipsTypesModel(BaseResponseModel):
    tips_types: List[TipTypeModel] = Field(alias="tipsTypes")


class BaseStatusModel(BaseModel):
    state: COICreationStatusModel


class CSGProductModel(BaseModel):
    product_id: str = Field(alias="productId")
    size_id: Optional[str] = Field(alias="sizeId")
    forbidden_modifiers: str = Field(alias="forbiddenModifiers")
    price_modification_amount: float = Field(alias="priceModificationAmount")


class CSGroupModel(IdNameModel):
    is_main_group: bool = Field(alias="isMainGroup")
    products: List[CSGProductModel]


class ComboSpecificationModel(BaseModel):
    source_action_id: str = Field(alias="sourceActionId")
    category_id: Optional[Any] = Field(alias="categoryId")
    name: str
    price_modification_type: int = Field(alias="priceModificationType")
    price_modification: float = Field(alias="priceModification")
    groups: List[CSGroupModel]


class BaseComboModel(BaseModel):
    combo_specifications: List[ComboSpecificationModel] = Field(alias="comboSpecifications")
    combo_categories: List[IdNameModel] = Field(alias="comboCategories")


class BaseComboCalculateModel(BaseModel):
    price: float
    incorrectly_filled_groups: List[str] = Field(alias="incorrectlyFilledGroups")


class BaseOrderByTableModel(BaseModel):
    pass


class EIEmployeeModel(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias='firstName')
    middle_name: Optional[str] = Field(alias='middleName')
    last_name: Optional[str] = Field(alias='lastName')
    email: Optional[str]
    phone: Optional[str]
    cell_phone: Optional[str] = Field(alias="cellPhone")


class BaseEInfoModel(BaseResponseModel):
    employee_info: EIEmployeeModel = Field(alias="employeeInfo")

class TypeRCI(Enum):
    phone = 'phone'
    card_track = 'cardTrack'
    card_number = 'cardNumber'
    email = 'email'
    id = 'id'

class CardCIModel(BaseModel):
    id: str
    track: str
    number: str
    valid_to_date: Optional[str] = Field(alias='validToDate')
class CategoriesCIModel(IdNameModel):
    is_active: bool = Field(alias="isActive")
    is_default_for_new_guests: bool = Field(alias="isDefaultForNewGuests")
class WalletBalanceCIModel(IdNameModel):
    type: int
    balance: float

class CustomerInfoModel(BaseModel):
    id: str
    referrer_id: Optional[str] = Field(alias='referrerId')
    name: Optional[str]
    surname: Optional[str]
    middle_name: Optional[str] = Field(alias="middleName")
    comment: Optional[str]
    phone: Optional[str]
    culture_name: Optional[str] = Field(alias="cultureName")
    birthday: Optional[str]
    email: Optional[str]
    sex: int
    consent_status: int = Field(alias="consentStatus")
    anonymized: bool
    cards: Optional[List[CardCIModel]]
    categories: Optional[List[CategoriesCIModel]]
    wallet_balances: Optional[List[WalletBalanceCIModel]] = Field(alias="walletBalances")
    user_data: Optional[str] = Field(alias="userData")
    shouldReceivePromoActionsInfo: Optional[bool] = Field(alias="shouldReceivePromoActionsInfo")
    shouldReceiveLoyaltyInfo: Optional[bool] = Field(alias="shouldReceiveLoyaltyInfo")
    shouldReceiveOrderStatusInfo: Optional[bool] = Field(alias="shouldReceiveOrderStatusInfo")
    personalDataConsentFrom: Optional[str] = Field(alias="personalDataConsentFrom")
    personalDataConsentTo: Optional[str] = Field(alias="personalDataConsentTo")
    personalDataProcessingFrom: Optional[str] = Field(alias="personalDataProcessingFrom")
    personalDataProcessingTo: Optional[str] = Field(alias="personalDataProcessingTo")
    isDeleted: Optional[bool] = Field(alias="isDeleted")

class CustomerCreateOrUpdateModel(BaseModel):
    id: str
class CustomerProgramAddResponse(BaseModel):
    user_wallet_id: str = Field(alias="userWalletId")
class ItemsTerminalGroupStopListResponse(BaseModel):
    balance: Decimal
    product_id: str = Field(alias="productId")
    size_id: Optional[str] = Field(alias="sizeId")
class ItemsTerminalGroupStopListsResponse(BaseModel):
    terminal_group_id: Optional[str] = Field(alias="terminalGroupId")
    items: Optional[List[ItemsTerminalGroupStopListResponse]]
class TerminalGroupStopListsResponse(BaseModel):
    organization_id: str = Field(alias='organizationId')
    items: Optional[List[ItemsTerminalGroupStopListsResponse]]

class StopListsResponse(BaseResponseModel):
    terminal_group_stop_lists: str = Field(alias="terminalGroupStopLists")

class RejectedItemsCSLResponse(BaseModel):
    balance: Decimal
    product_id: str = Field(alias="productId")
    size_id: Optional[str] = Field(alias="sizeId")

class CheckStopListsResponse(BaseResponseModel):
    rejected_items: Optional[List[RejectedItemsCSLResponse]] = Field(alias="rejectedItems")