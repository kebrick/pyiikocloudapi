from pydantic import BaseModel, Field
from typing import Optional, List, Union


class BaseResponseModel(BaseModel):
    correlation_id: Optional[str] = Field(alias='correlationId')


class ErrorModel(BaseResponseModel):
    error_description: Optional[str] = Field(alias='errorDescription')
    error: Optional[str]


class OrganizationsModel(BaseModel):
    name: str
    id: str


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


class PaymentTypeModel(BaseModel):
    id: str
    name: str
    kind: str


class PaymentItemOrderModel(BaseModel):
    payment_type: PaymentTypeModel = Field(alias="paymentType")
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
    payment_type: PaymentTypeModel = Field(alias="paymentType")
    sum: float
    is_preliminary: bool = Field(alias="isPreliminary")
    is_external: bool = Field(alias="isExternal")
    is_processed_externally: bool = Field(alias="isProcessedExternally")
    is_fiscalized_externally: Optional[bool] = Field(alias="isFiscalizedExternally")


class DiscountTypeModel(BaseModel):
    id: str
    name: str


class DiscountsItemOrderModel(BaseModel):
    discount_type: DiscountTypeModel = Field(alias="discountType")
    sum: float
    selective_positions: Optional[List[str]] = Field(alias="selectivePositions")


class OrderTypeModel(BaseModel):
    id: str
    name: str
    order_service_type: str = Field(alias="orderServiceType")


class OrderModel(BaseModel):
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
    items: List[dict]
    combos: Optional[List[CombosItemOrderModel]]
    payments: Optional[List[PaymentItemOrderModel]]
    tips: Optional[List[TipsItemOrderModel]]
    discounts: Optional[List[DiscountsItemOrderModel]]
    order_type: Optional[OrderTypeModel] = Field(alias="orderType")
    terminal_group_id: str = Field(alias="terminalGroupId")
    processed_payments_sum: Optional[int] = Field(alias="processedPaymentsSum")


class ErrorInfoModel(BaseModel):
    # "code": "Common",
    # "message": "string",
    # "description": "string",
    # "additionalData": null
    code: str
    message: str
    description: str
    additional_data: Optional[Union[str, list]] = Field(alias="additionalData")


class OrderItemModel(BaseModel):
    id: str
    external_number: Optional[str] = Field(alias='externalNumber')
    organization_id: str = Field(alias='organizationId')
    timestamp: int
    creation_status: Optional[str] = Field(alias='creationStatus')
    error_info: Optional[ErrorInfoModel] = Field(alias='errorInfo')
    order: Optional[OrderModel]

    def get_by_courier_id(self, courier_id: str):
        # return next(i for i in self.orders if i.order.courier_info is not None and str(i.order.courier_info.courier.id) == courier_id)

        return self if self.order.courier_info is not None and self.order.courier_info.courier.id == courier_id else None


class ByIdModel(BaseResponseModel):
    orders: Optional[List[OrderItemModel]]


class OrdersByOrganizationsModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    orders: Optional[List[OrderItemModel]]

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


class TerminalGroupsItemModel(BaseModel):
    id: str
    name: str
    organization_id: str = Field(alias="organizationId")
    address: Optional[str]


class TerminalGroupsModel(BaseModel):
    organization_id: str = Field(alias='organizationId')
    items: Optional[List[TerminalGroupsItemModel]]


class BaseTerminalGroupsModel(BaseResponseModel):
    terminal_groups: Optional[List[TerminalGroupsModel]] = Field(alias="terminalGroups")


class TGIsAliveItemModel(BaseModel):
    isAlive: bool = Field(alias="isAlive")
    terminal_group_id: str = Field(alias="terminalGroupId")
    organization_id: str = Field(alias='organizationId')


class BaseTGIsAliveyModel(BaseResponseModel):
    is_alive_status: Optional[List[StreetsItemModel]] = Field(alias="isAliveStatus")


class COrderCustomerModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    comment: Optional[str]
    birthdate: Optional[str]
    email: Optional[str]
    should_receive_order_status_notifications: Optional[bool] = Field(alias="shouldReceiveOrderStatusNotifications")
    gender: Optional[str]


class COrderGuestsModel(BaseModel):
    count: int


class COrderModel(BaseModel):
    id: Optional[str]
    external_number: Optional[str] = Field(alias='externalNumber')
    table_ids: Optional[List[str]]
    customer: Optional[CustomerModel]
    phone: Optional[str]
    guests: Optional[COrderGuestsModel]
    tab_name: Optional[str] = Field(alias="tabName")


class COrderSettings(BaseModel):
    transport_to_front_timeout: int = Field(alias="transportToFrontTimeout", default=0)


class BaseCOrderRequestModel(BaseModel):
    organization_id: str = Field(alias="organizationId")
    terminal_group_id: str = Field(alias="terminalGroupId")
    order: COrderModel
    createOrderSettings: COrderSettings
