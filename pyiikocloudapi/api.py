import datetime
import json
import logging
import pprint
import uuid
from datetime import date, timedelta
from datetime import datetime

import requests

from pyiikocloudapi.decorators import experimental
from pyiikocloudapi.exception import CheckTimeToken, SetSession, TokenException, PostException, ParamSetException
from pyiikocloudapi.models import *


class BaseAPI:
    DEFAULT_TIMEOUT = "15"

    # __BASE_URL = "https://api-ru.iiko.services"

    def __init__(self, api_login: str, session: Optional[requests.Session] = None, debug: bool = False,
                 base_url: str = None, working_token: str = None, base_headers: dict = None, logger: Optional[
            logging.Logger] = None, return_dict: bool = False):
        """

        :param api_login: login api iiko cloud
        :param session: session object
        :param debug: logging dict response
        :param base_url: url iiko cloud api
        :param working_token: Initialize an object based on a working token, that is, without requesting a new one
        :param base_headers: base header for request in iiko cloud api
        :param logger: your object Logger
        :param return_dict: return a dictionary instead of models
        """

        if session is not None:
            self.__session = session
        else:
            self.__session = requests.Session()

        self.__api_login = api_login
        self.__token: Optional[str] = None
        self.__debug = debug
        self.__time_token: Optional[date] = None
        self.__organizations_ids_model: Optional[BaseOrganizationsModel] = None
        self.__organizations_ids: Optional[List[str]] = None
        self.__strfdt = "%Y-%m-%d %H:%M:%S.000"
        self.__return_dict = return_dict
        self.logger = logger if logger is not None else logging.getLogger()

        self.__base_url = "https://api-ru.iiko.services" if base_url is None else base_url
        self.__headers = {
            "Content-Type": "application/json",
            "Timeout": "45",
        } if base_headers is None else base_headers
        self.__set_token(working_token) if working_token is not None else self.__get_access_token()
        # if working_token is not None:
        #     self.__set_token(working_token)
        # else:
        #     self.__get_access_token()
        self.__last_data = None

    def check_status_code_token(self, code: Union[str, int]):
        if str(code) == "401":
            self.__get_access_token()
        elif str(code) == "400":
            pass
        elif str(code) == "408":
            pass
        elif str(code) == "500":
            pass

    def check_token_time(self) -> bool:
        """
        Проверка на время жизни маркера доступа
        :return: Если прошло 15 мин будет запрошен токен и метод вернёт True, иначе вернётся False
        """
        fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)
        time_token = self.__time_token
        try:

            if time_token <= fifteen_minutes_ago:
                self.__get_access_token()
                return True
            else:
                return False
        except TypeError:
            raise CheckTimeToken(
                self.__class__.__qualname__,
                self.check_token_time.__name__,
                f"Не запрошен Token и не присвоен объект типа datetime.datetime")

    @property
    def organizations_ids_models(self) -> Optional[List[OrganizationModel]]:
        return self.__organizations_ids_model

    @property
    def organizations_ids(self) -> Optional[List[str]]:
        return self.__organizations_ids

    @property
    def last_data(self) -> Optional[List[str]]:
        return self.__last_data

    @property
    def session_s(self) -> requests.Session:
        """Вывести сессию"""
        return self.__session

    @session_s.setter
    def session_s(self, session: requests.Session = None):
        """Изменение сессии"""
        if session is None:
            raise SetSession(
                self.__class__.__qualname__,
                self.session_s.__name__,
                f"Не присвоен объект типа requests.Session")
        else:
            self.__session = session

    @property
    def time_token(self):
        return self.__time_token

    @property
    def api_login(self) -> str:
        return self.__api_login

    @property
    def token(self) -> str:
        return self.__token

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, value: str):
        self.__base_url = value

    @property
    def strfdt(self):
        return self.__strfdt

    @strfdt.setter
    def strfdt(self, value: str):
        self.__strfdt = value

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value: str):
        self.__headers = value

    @property
    def return_dict(self):
        return self.__return_dict

    @headers.setter
    def headers(self, value: str):
        self.__return_dict = value

    @property
    def timeout(self):
        return self.__headers.get("Timeout")

    @timeout.setter
    def timeout(self, value: int):
        self.__headers.update({"Timeout": str(value)})

    @timeout.deleter
    def timeout(self):
        self.__headers.update({"Timeout": str(self.DEFAULT_TIMEOUT)})

    def __set_token(self, token):
        self.__token = token
        self.__headers["Authorization"] = f"Bearer {self.token}"
        self.__time_token = datetime.now()

    def access_token(self):
        """Получить маркер доступа"""
        data = json.dumps({"apiLogin": self.api_login})
        try:
            result = self.session_s.post(f'{self.__base_url}/api/1/access_token', json=data)

            response_data: dict = json.loads(result.content)
            if response_data.get("errorDescription", None) is not None:
                raise TypeError(f'{response_data=}')

            if response_data.get("token", None) is not None:
                self.check_status_code_token(result.status_code)
                self.__set_token(response_data.get("token", ""))

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.access_token.__name__,
                                 f"Не удалось получить маркер доступа: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.access_token.__name__,
                                 f"Не удалось получить маркер доступа: \n{err}")

    def _post_request(self, url: str, data: dict = None, timeout=DEFAULT_TIMEOUT, model_response_data=None,
                      model_error=CustomErrorModel):
        if data is None:
            data = {}
        if timeout != self.DEFAULT_TIMEOUT:
            self.timeout = timeout
        self.logger.info(f"{url=}, {data=}, {model_response_data=}, {model_error=}")
        response = self.session_s.post(f'{self.base_url}{url}', data=json.dumps(data),
                                       headers=self.headers)
        if response.status_code == 401:
            self.__get_access_token()
            return self._post_request(url=url, data=data, timeout=timeout, model_response_data=model_response_data,
                                      model_error=model_error)

        if self.__debug:
            try:

                self.logger.debug(
                    f"Входные данные:\n{response.request.url=}\n{response.request.body=}\n{response.request.headers=}\n\nВыходные данные:\n{response.headers=}\n{response.content=}\n\n")
            except Exception as err:
                self.logger.debug(f"{err=}")
        response_data: dict = json.loads(response.content)
        self.__last_data = response_data
        if self.__return_dict:
            return response_data
        if response_data.get("errorDescription", None) is not None:
            error_model = model_error.parse_obj(response_data)
            error_model.status_code = response.status_code
            return error_model
        if model_response_data is not None:
            return model_response_data.parse_obj(response_data)
        del self.timeout
        return response_data

    def __get_access_token(self):
        out = self.access_token()
        if isinstance(out, CustomErrorModel):
            raise TokenException(self.__class__.__qualname__,
                                 self.access_token.__name__,
                                 f"Не удалось получить маркер доступа: \n{out}")

    def __convert_org_data(self, data: BaseOrganizationsModel):
        self.__organizations_ids = data.__list_id__()

    def organizations(self, organization_ids: List[str] = None, return_additional_info: bool = None,
                      include_disabled: bool = None, timeout=DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseOrganizationsModel]:
        """
        Возвращает организации, доступные пользователю API-login.
        :param organization_ids: Organizations IDs which have to be returned. By default - all organizations from apiLogin.
        :param return_additional_info: A sign whether additional information about the organization should be returned (RMS version, country, restaurantAddress, etc.), or only minimal information should be returned (id and name).
        :param include_disabled: Attribute that shows that response contains disabled organizations.
        :return:
        """
        #         https://api-ru.iiko.services/api/1/organizations
        data = {}
        if organization_ids is not None:
            data["organizationIds"] = organization_ids
        if return_additional_info is not None:
            data["returnAdditionalInfo"] = return_additional_info
        if include_disabled is not None:
            data["includeDisabled"] = include_disabled
        try:

            response_data = self._post_request(
                url="/api/1/organizations",
                data=data,
                model_response_data=BaseOrganizationsModel,
                timeout=timeout
            )
            if isinstance(response_data, BaseOrganizationsModel):
                self.__convert_org_data(data=response_data)
            return response_data


        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.organizations.__name__,
                                 f"Не удалось получить организации: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.organizations.__name__,
                            f"Не удалось получить организации: \n{err}")
class WebHook(BaseAPI):
    @staticmethod
    def parse_webhook_order(data: List[dict]) -> List[WebHookDeliveryOrderEventInfoModel]:
        return [WebHookDeliveryOrderEventInfoModel.parse_obj(order_info) for order_info in data]
    @staticmethod
    def parse_webhook_reserve(data: List[dict]) -> List[WebHookDeliveryOrderEventInfoModel]:
        raise FutureWarning('In developing!')



class Commands(BaseAPI):
    def status(self, organization_id: str, correlation_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        BaseStatusModel, CustomErrorModel,]:
        """


        :param organization_id:
        :param correlation_id:
        :param timeout:
        :return:
        """
        data = {
            "organizationId": organization_id,
            "correlationId": correlation_id,
        }

        try:

            return self._post_request(
                url="/api/1/commands/status",
                data=data,
                model_response_data=BaseStatusModel,
                timeout=timeout

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.status.__name__,
                                 f"Не удалось получить статус: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.status.__name__,
                            f"Не удалось получить статус: \n{err}")


class Dictionaries(BaseAPI):
    def cancel_causes(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseCancelCausesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.cancel_causes.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return self._post_request(
                url="/api/1/cancel_causes",
                data=data,
                model_response_data=BaseCancelCausesModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.cancel_causes.__name__,
                                 f"Не удалось получить причины отмены доставки: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.cancel_causes.__name__,
                            f"Не удалось получить причины отмены доставки: \n{err}")

    def order_types(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseOrderTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.order_types.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return self._post_request(
                url="/api/1/deliveries/order_types",
                data=data,
                model_response_data=BaseOrderTypesModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.order_types.__name__,
                                 f"Не удалось получить типы заказа: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.order_types.__name__,
                            f"Не удалось получить типы заказа: \n{err}")

    def discounts(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseDiscountsModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.discounts.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return self._post_request(
                url="/api/1/discounts",
                data=data,
                model_response_data=BaseDiscountsModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.discounts.__name__,
                                 f"Не удалось получить скидки/надбавки: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.discounts.__name__,
                            f"Не удалось получить скидки/надбавки: \n{err}")

    def payment_types(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BasePaymentTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.payment_types.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return self._post_request(
                url="/api/1/payment_types",
                data=data,
                model_response_data=BasePaymentTypesModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.payment_types.__name__,
                                 f"Не удалось получить типы оплаты: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.payment_types.__name__,
                            f"Не удалось получить типы оплаты: \n{err}")

    def removal_types(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseRemovalTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.removal_types.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return self._post_request(
                url="/api/1/removal_types",
                data=data,
                model_response_data=BaseRemovalTypesModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.removal_types.__name__,
                                 f"Не удалось получить removal_types: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.removal_types.__name__,
                            f"Не удалось получить removal_types: \n{err}")

    def tips_types(self, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel, BaseTipsTypesModel]:
        try:

            return self._post_request(
                url="/api/1/tips_types",
                model_response_data=BaseTipsTypesModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.removal_types.__name__,
                                 f"Не удалось получить подсказки для группы api-logins rms: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.removal_types.__name__,
                            f"Не удалось получить подсказки для группы api-logins rms: \n{err}")


class DiscountPromotion(BaseAPI):
    def coupons_series(self, organization_id: str) -> Union[
        CustomErrorModel, SeriesWithNotActivatedCoupon]:
        if not bool(organization_id):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.coupons_series.__name__,
                                    f"Отсутствует аргумент id организации")
        data = {
            "organizationId": organization_id,
        }
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/coupons/series",
                data=data,
                model_response_data=SeriesWithNotActivatedCoupon,
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.coupons_series.__name__,
                                 f"Не удалось получить промокоды: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.coupons_series.__name__,
                            f"Не удалось получить промокоды: \n{err}")

    def coupons_info(self, organization_id: str, number: str, series: str = None) -> Union[
        CustomErrorModel, BaseCouponInfo]:
        if not bool(organization_id):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.coupons_info.__name__,
                                    f"Отсутствует аргумент id организации")
        data = {
            "number": number,
            "series": series,
            "organizationId": organization_id,
        }
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/coupons/info",
                data=data,
                model_response_data=BaseCouponInfo,
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.coupons_info.__name__,
                                 f"Не удалось получить промокоды: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.coupons_info.__name__,
                            f"Не удалось получить промокоды: \n{err}")


class Menu(BaseAPI):
    def nomenclature(self, organization_id: str, start_revision: int = None, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseNomenclatureModel]:
        data = {
            "organizationId": organization_id,
        }
        if start_revision is not None:
            data["startRevision"] = start_revision

        try:

            return self._post_request(
                url="/api/1/nomenclature",
                data=data,
                model_response_data=BaseNomenclatureModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.nomenclature.__name__,
                                 f"Не удалось получить номенклатуру: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.nomenclature.__name__,
                            f"Не удалось получить номенклатуру: \n{err}")

    def menu(self, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel, BaseMenuModel]:
        try:

            return self._post_request(
                url="/api/2/menu",
                model_response_data=BaseMenuModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.nomenclature.__name__,
                                 f"Не удалось получить внешние меню с ценовыми категориями: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.nomenclature.__name__,
                            f"Не удалось получить внешние меню с ценовыми категориями: \n{err}")

    def menu_by_id(self, external_menu_id: str, organization_ids: List[str], price_category_id: str = None,
                   timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseMenuByIdModel]:

        data = {
            "externalMenuId": external_menu_id,
            "organizationIds": organization_ids,
        }

        if price_category_id is not None:
            data["priceCategoryId"] = price_category_id

        try:

            return self._post_request(
                url="/api/2/menu/by_id",
                data=data,
                model_response_data=BaseMenuByIdModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.menu_by_id.__name__,
                                 f"Не удалось получить внешнее меню по ID.: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.menu_by_id.__name__,
                            f"Не удалось получить внешнее меню по ID.: \n{err}")
    def stop_lists(self, organization_ids: List[str], return_size: bool = False,
                   terminal_groups_ids: List[str] = None,
                   timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, StopListsResponse]:

        data = {
            "organizationIds": organization_ids,
            "returnSize": return_size,
        }

        if terminal_groups_ids is not None:
            data["terminalGroupsIds"] = terminal_groups_ids

        try:

            return self._post_request(
                url="/api/1/stop_lists",
                data=data,
                model_response_data=StopListsResponse,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.stop_lists.__name__,
                                 f"Не удалось получить товары, которых нет в наличии: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.stop_lists.__name__,
                            f"Не удалось получить товары, которых нет в наличии: \n{err}")
    def stop_lists_check(self, organization_id: str,  terminal_group_id: str,
                         items: dict,
                   timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, CheckStopListsResponse]:
        """"""

        data = {
            "organizationId": organization_id,
            "terminalGroupId": terminal_group_id,
            "items": items
        }

        try:

            return self._post_request(
                url="/api/1/stop_lists/check",
                data=data,
                model_response_data=CheckStopListsResponse,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.stop_lists_check.__name__,
                                 f"Не удалось проверить товары в списке отсутствующих на складе.: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.stop_lists_check.__name__,
                            f"Не удалось проверить товары в списке отсутствующих на складе.: \n{err}")

    def combo(self, organization_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel, BaseComboModel]:

        data = {
            "organizationId": organization_id,
        }

        try:

            return self._post_request(
                url="/api/1/combo",
                data=data,
                model_response_data=BaseComboModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.nomenclature.__name__,
                                 f"Не удалось получить комбо: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.nomenclature.__name__,
                            f"Не удалось получить комбо: \n{err}")

    def combo_calculate(self, organization_id: str, items: dict, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseComboCalculateModel]:

        data = {
            "items": items,
            "organizationId": organization_id,
        }

        try:

            return self._post_request(
                url="/api/1/combo/calculate",
                data=data,
                model_response_data=BaseComboCalculateModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.nomenclature.__name__,
                                 f"Не удалось получить расчёт комбо: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.nomenclature.__name__,
                            f"Не удалось получить расчёт комбо: \n{err}")


class TerminalGroup(BaseAPI):
    def terminal_groups(self, organization_ids: List[str], include_disabled: bool = False,
                        timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel,
                                                                  BaseTerminalGroupsModel]:
        """

        :param organization_ids: 	Array of strings <uuid>, Organizations IDs for which information is requested.
        :param include_disabled:
        :return:
        """
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.terminal_groups.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        if include_disabled:
            data["includeDisabled"] = include_disabled
        try:

            return self._post_request(
                url="/api/1/terminal_groups",
                data=data,
                model_response_data=BaseTerminalGroupsModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.terminal_groups.__name__,
                                 f"Не удалось получить регионы: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.terminal_groups.__name__,
                            f"Не удалось получить регионы: \n{err}")

    def is_alive(self, organization_ids: List[str], terminal_group_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> \
        Union[CustomErrorModel,
              BaseTGIsAliveyModel]:
        """

        :param terminal_group_ids:
        :param organization_ids: 	Array of strings <uuid>, Organizations IDs for which information is requested.
        :return:
        """
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.is_alive.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
            "terminalGroupIds": terminal_group_ids
        }

        try:

            return self._post_request(
                url="/api/1/terminal_groups/is_alive",
                data=data,
                model_response_data=BaseTGIsAliveyModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.is_alive.__name__,
                                 f"Не удалось получить регионы: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.is_alive.__name__,
                            f"Не удалось получить регионы: \n{err}")


class Address(BaseAPI):
    def regions(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseRegionsModel]:
        """
        Возвращает регионы, доступные пользователю API-login.
        :return:
        """
        #         https://api-ru.iiko.services/api/1/organizations
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.regions.__name__,
                                    f"Пустой список id организаций")

        data = {
            "organizationIds": organization_ids,
        }
        try:

            return self._post_request(
                url="/api/1/regions",
                data=data,
                model_response_data=BaseRegionsModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.regions.__name__,
                                 f"Не удалось получить регионы: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.regions.__name__,
                            f"Не удалось получить регионы: \n{err}")

    def cities(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseCitiesModel]:
        """
        Возвращает регионы, доступные пользователю API-login.
        :return:
        """
        #         https://api-ru.iiko.services/api/1/organizations
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.cities.__name__,
                                    f"Пустой список id организаций")

        data = {
            "organizationIds": organization_ids,
        }
        try:

            return self._post_request(
                url="/api/1/cities",
                data=data,
                model_response_data=BaseCitiesModel,
                timeout=timeout
            )


        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.cities.__name__,
                                 f"Не удалось получить города: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.cities.__name__,
                            f"Не удалось получить города: \n{err}")

    def by_city(self, organization_id: str, city_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseStreetByCityModel]:
        """
        Возвращает регионы, доступные пользователю API-login.
        :return:
        """
        #         https://api-ru.iiko.services/api/1/organizations

        data = {
            "organizationId": organization_id,
            "cityId": city_id
        }
        try:

            return self._post_request(
                url="/api/1/streets/by_city",
                data=data,
                model_response_data=BaseStreetByCityModel,
                timeout=timeout
            )


        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.cities.__name__,
                                 f"Не удалось получить улицы: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.cities.__name__,
                            f"Не удалось получить улицы: \n{err}")


class DeliveryRestrictions(BaseAPI):
    def delivery_restrictions(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel,]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.delivery_restrictions.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }

        try:

            return self._post_request(
                url="/api/1/delivery_restrictions",
                data=data,
                timeout=timeout
                # model_response_data=BaseRemovalTypesModel
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.delivery_restrictions.__name__,
                                 f"Не удалось получить список ограничений доставки: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.delivery_restrictions.__name__,
                            f"Не удалось получить список ограничений доставки: \n{err}")

    def dr_allowed(self, organization_ids: List[str], is_courier_delivery: bool,
                   delivery_address: dict = None, order_location: dict = None, order_items: dict = None,
                   delivery_date: str = None, delivery_sum: float = None, discount_sum: float = None,
                   timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseRemovalTypesModel]:
        """
        Get suitable terminal groups for delivery restrictions.
        :param organization_ids:
        :param is_courier_delivery:
        :param delivery_address:
        :param order_location:
        :param order_items:
        :param delivery_date:
        :param delivery_sum:
        :param discount_sum:
        :param timeout:
        :return:
        """
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.dr_allowed.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
            "isCourierDelivery": is_courier_delivery,
        }
        if delivery_address is not None:
            data["deliveryAddress"] = delivery_address
        if order_location is not None:
            data["orderLocation"] = order_location
        if order_items is not None:
            data["orderItems"] = order_items
        if delivery_date is not None:
            data["deliveryDate"] = delivery_date
        if delivery_sum is not None:
            data["deliverySum"] = delivery_sum
        if discount_sum is not None:
            data["discountSum"] = discount_sum
        try:

            return self._post_request(
                url="/api/1/delivery_restrictions/allowed",
                data=data,
                timeout=timeout,
                model_response_data=DeliveryRestrictionsAllowedModel
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.dr_allowed.__name__,
                                 f"Не удалось получить подходящие группы терминалов для ограничения доставки: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.dr_allowed.__name__,
                            f"Не удалось получить подходящие группы терминалов для ограничения доставки: \n{err}")


class Orders(BaseAPI):
    def order_create(self, organization_id: str, terminal_group_id: str, order: dict,
                     create_order_settings: Optional[int] = None, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel,
        BaseCreatedOrderInfoModel]:
        """"""

        data = {
            "organizationId": organization_id, #'organizationId' instead of 'organizationIds'. 'errorDescription': "Required property 'organizationId' not found in JSON.
            "terminalGroupId": terminal_group_id,
            "order": order,
        }
        if create_order_settings is not None:
            data["createOrderSettings"] = create_order_settings

        try:

            return self._post_request(
                url="/api/1/order/create",
                data=data,
                model_response_data=BaseCreatedOrderInfoModel,
                timeout=timeout

            )
        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.order_create.__name__,
                                f"Не удалось создать заказ из за: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.order_create.__name__,
                            f"Не удалось создать заказ из за: \n{err}")

    def order_by_id(self,
                    organization_ids: List[str],
                    order_ids: List[str] = None,
                    pos_order_ids: List[str] = None,
                    return_external_data_keys: List[str] = None,
                    source_keys: list = None, timeout=BaseAPI.DEFAULT_TIMEOUT
                    ) -> Union[CustomErrorModel, ByIdModel]:
        """
        Получить заказы по идентификаторам.

        :param organization_ids: Organization IDs
        :param order_ids: list
        :param pos_order_ids: list
        :param return_external_data_keys: list
        :param source_keys:
        :return:
        """
        # https://api-ru.iiko.services/api/1/deliveries/by_id

        data = {
            "organizationIds": organization_ids,
            "orderIds": order_ids,
        }
        if(source_keys is not None):
            data["sourceKeys"] = source_keys

        if(pos_order_ids is not None):
            data["posOrderIds"] = pos_order_ids

        if(return_external_data_keys is not None):
            data["returnExternalDataKeys"] = return_external_data_keys

        try:

            return self._post_request(
                url="/api/1/order/by_id",
                data=data,
                model_response_data=ByIdModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.order_by_id.__name__,
                                 f"Не удалось получить заказы: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.order_by_id.__name__,
                                 f"Не удалось: \n{err}")

    def order_by_table(self,
                       organization_ids: List[str],
                       table_ids: List[str],
                       source_keys: List[str] = None,
                       statuses: List[str] = None,
                       date_from: str = None,
                       date_to: str = None, timeout=BaseAPI.DEFAULT_TIMEOUT
                       ) -> Union[CustomErrorModel, ByIdModel]:
        """

        :param organization_ids:
        :param table_ids:
        :param source_keys:
        :param statuses:
        :param date_from:
        :param date_to:
        :return:
        """
        # https://api-ru.iiko.services/api/1/deliveries/by_id
        if not isinstance(table_ids, list):
            raise TypeError("type table_ids != list")

        data = {
            "organizationIds": organization_ids,
            "tableIds": table_ids,
        }

        if source_keys is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type source_keys != list")
            data["sourceKeys"] = source_keys

        if statuses is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type statuses != list")
            data["statuses"] = statuses

        if date_from is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type date_from != str")
            data["dateFrom"] = date_from

        if date_to is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type date_to != str")
            data["dateTo"] = date_to

        try:

            return self._post_request(
                url="/api/1/order/by_table",
                data=data,
                model_response_data=ByIdModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.order_by_id.__name__,
                                 f"Не удалось получить заказы: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.order_by_id.__name__,
                                 f"Не удалось: \n{err}")


class Deliveries(BaseAPI):
    def delivery_create(self, organization_id: str, order: dict, terminal_group_id: str = None,
                        create_order_settings: Optional[int] = None, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseCreatedDeliveryOrderInfoModel]:
        """"""
        data = {
            "organizationId": organization_id,
            "order": order,
        }
        if terminal_group_id is not None:
            data["terminalGroupId"] = terminal_group_id

        if create_order_settings is not None:
            data["createOrderSettings"] = {"transportToFrontTimeout": create_order_settings}

        try:

            return self._post_request(
                url="/api/1/deliveries/create",
                data=data,
                model_response_data=BaseCreatedDeliveryOrderInfoModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.delivery_create.__name__,
                                f"Не удалось создать заказ из за: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.delivery_create.__name__,
                            f"Не удалось создать заказ из за: \n{err}")

    def update_order_delivery_status(self,
                                     organization_id: List[str],
                                     order_id: str,
                                     delivery_status: str = "Delivered",
                                     delivery_date: datetime = datetime.now(), timeout=BaseAPI.DEFAULT_TIMEOUT
                                     ):
        """
        :param organization_id: Organization ID
        :param order_id: Order ID.
        :param delivery_status: Enum: "Waiting" "OnWay" "Delivered", Delivery status. Can be only switched between these three statuses.
        :param delivery_date: The date and time when the order was received by the guest (Local for delivery terminal). This field must be filled in only if the order is transferred to the "Delivered" status.

        :return:
        """
        #         https://api-ru.iiko.services/api/1/deliveries/update_order_delivery_status
        if not isinstance(delivery_date, datetime):
            raise TypeError("delivery_date != datetime")
        data = {
            "organizationIds": organization_id,
            "orderId": order_id,
            "deliveryStatus": delivery_status,
        }
        if delivery_status == "Delivered":
            data["deliveryDate"] = delivery_date.strftime(self.strfdt)
        try:

            return self._post_request(
                url="/api/1/deliveries/update_order_delivery_status",
                data=data,
                model_response_data=BaseResponseModel,
                timeout=timeout
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.update_order_delivery_status.__name__,
                                 f"Не удалось изменить статус: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.update_order_delivery_status.__name__,
                                 f"Не удалось: \n{err}")

    def confirm(self,
                organization_id: List[str],
                order_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT
                ):
        """
        Подвердить статус доставки заказа

        :param organization_id: Organization ID
        :param order_id: Order ID.
        :return: dict response
        """
        #         https://api-ru.iiko.services/api/1/deliveries/confirm
        data = {
            "organizationIds": organization_id,
            "orderId": order_id,
        }

        try:
            return self._post_request(
                url="/api/1/deliveries/confirm",
                data=data,
                model_response_data=BaseResponseModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.confirm.__name__,
                                 f"Не удалось изменить статус: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.confirm.__name__,
                                 f"Не удалось: \n{err}")

    def cancel_confirmation(self,
                            organization_id: List[str],
                            order_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT
                            ):
        """
        Отменить подтверждение доставки

        :param organization_id: Organization ID
        :param order_id: Order ID.
        :return: dict response
        """
        # https://api-ru.iiko.services/api/1/deliveries/cancel_confirmation
        data = {
            "organizationIds": organization_id,
            "orderId": order_id,
        }

        try:

            return self._post_request(
                url="/api/1/deliveries/cancel_confirmation",
                data=data,
                model_response_data=BaseResponseModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.cancel_confirmation.__name__,
                                 f"Не удалось изменить статус: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.cancel_confirmation.__name__,
                                 f"Не удалось: \n{err}")

    def by_delivery_date_and_status(self,
                                    organization_id: List[str],
                                    delivery_date_from: Union[datetime, str],
                                    delivery_date_to: Union[datetime, str] = None,
                                    statuses: list = None,
                                    source_keys: list = None, timeout=BaseAPI.DEFAULT_TIMEOUT
                                    ) -> Union[ByDeliveryDateAndStatusModel, CustomErrorModel]:
        """


        :param organization_id:
        :param delivery_date_from: datetime or "%Y-%m-%d %H:%M:%S.%f". Order delivery date (Local for delivery terminal). Lower limit.
        :param delivery_date_to: datetime or "%Y-%m-%d %H:%M:%S.%f". Order delivery date (Local for delivery terminal). Upper limit.
        :param statuses: Items Enum: "Unconfirmed", "WaitCooking", "ReadyForCooking", "CookingStarted", "CookingCompleted", "Waiting", "OnWay", "Delivered", "Closed", "Cancelled",  Allowed order statuses.
        :param source_keys:Source keys.
        :return:
        """
        # https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_status
        data = {
            "organizationIds": organization_id,
        }
        if isinstance(delivery_date_from, datetime):
            data["deliveryDateFrom"] = delivery_date_from.strftime(self.strfdt)
        elif isinstance(delivery_date_from, str):
            data["deliveryDateFrom"] = delivery_date_from

        if isinstance(delivery_date_to, datetime):
            data["deliveryDateTo"] = delivery_date_to.strftime(self.strfdt)
        elif isinstance(delivery_date_to, str):
            data["deliveryDateTo"] = delivery_date_to
        if delivery_date_to is not None:
            if isinstance(delivery_date_to, datetime):
                data["deliveryDateTo"] = delivery_date_to.strftime(self.strfdt)
            elif isinstance(delivery_date_to, str):
                data["deliveryDateTo"] = delivery_date_to
            else:
                raise TypeError("type delivery_date_to != datetime or str")

        if statuses is not None:
            if not isinstance(statuses, list):
                raise TypeError("type statuses != list")
            data["statuses"] = statuses

        if source_keys is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type source_keys != list")
            data["sourceKeys"] = source_keys

        try:
            # result = self.session_s.post(f'{self.base_url}/api/1/deliveries/by_delivery_date_and_status',
            #                              json=json.dumps(data),
            #                              headers=self.headers)
            # out: dict = json.loads(result.content)
            # print(out)
            # if out.get("errorDescription", None) is not None:
            #     # raise PostException(self.__class__.__qualname__,
            #     #                     self.by_delivery_date_and_status.__name__,
            #     #                     f"Не удалось получить заказы: \n{out}")
            #     return ErrorModel.parse_obj(out)
            # return ByDeliveryDateAndStatusModel.parse_obj(out)
            return self._post_request(
                url="/api/1/deliveries/by_delivery_date_and_status",
                data=data,
                model_response_data=ByDeliveryDateAndStatusModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.by_delivery_date_and_status.__name__,
                                 f"Не удалось получить заказы: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.by_delivery_date_and_status.__name__,
                                 f"Не удалось: \n{err}")

    @experimental("будет дописан в будущем!")
    def by_revision(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        # Retrieve list of orders changed from the time revision was passed.
        # https://api-ru.iiko.services/api/1/deliveries/by_revision
        pass

    @experimental("будет дописан в будущем!")
    def by_delivery_date_and_phone(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        # Retrieve list of orders changed from the time revision was passed.
        # https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_phone
        pass

    def by_delivery_date_and_source_key_and_filter(self,
                                                   organization_id: List[str],
                                                   terminal_group_ids: Optional[List[Union[str, uuid.UUID]]] = None,
                                                   delivery_date_from: Optional[str] = None,
                                                   delivery_date_to: Optional[str] = None,
                                                   statuses: Optional[List[str]] = None,
                                                   has_problem: Optional[bool] = None,
                                                   order_service_type: Optional[str] = None,
                                                   search_text: Optional[str] = None,
                                                   time_to_cooking_error_timeout: Optional[int] = None,
                                                   cooking_timeout: Optional[int] = None,
                                                   sort_property: Optional[str] = None,
                                                   sort_direction: Optional[str] = None,
                                                   rows_count: Optional[int] = None,
                                                   source_keys: Optional[List[str]] = None,
                                                   order_ids: Optional[List[Union[str, uuid.UUID]]] = None,
                                                   timeout=BaseAPI.DEFAULT_TIMEOUT
                                                   ):
        """

        :param organization_id: List
        :param terminal_group_ids: List of terminal groups IDs.
        :param delivery_date_from: Order delivery date (Local for delivery terminal). Lower limit.
        :param delivery_date_to: Order delivery date (Local for delivery terminal). Upper limit.
        :param statuses: Enum: "Unconfirmed" "WaitCooking" "ReadyForCooking" "CookingStarted" "CookingCompleted" "Waiting" "OnWay" "Delivered" "Closed" "Cancelled", Array of strings (iikoTransport.PublicApi.Contracts.Deliveries.Common.DeliveryStatus) Nullable
        :param has_problem: If true, delivery has a problem
        :param order_service_type: Order service type. Enum: "DeliveryByCourier" "DeliveryByClient"
        :param search_text: Value for search. Used for prefix search.
        :param time_to_cooking_error_timeout: Error timeout for status time to cooking, in seconds.
        :param cooking_timeout: Expected cooking time, in seconds.
        :param sort_property:  Enum: ("Number", "CompleteBefore", "Sum", "Customer", "Courier", "Status"),  Sorting property.
        :param sort_direction: Enum: ("Ascending", "Descending"),  Sorting direction.
        :param rows_count: Maximum number of items returned.
        :param source_keys: Source keys.
        :param order_ids: Order IDs
        :return:
        """

        #         https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_source_key_and_filter
        data = {
            "organizationIds": organization_id,
        }

        if terminal_group_ids is not None:
            if not isinstance(terminal_group_ids, list):
                raise TypeError("type terminal_group_ids != list")
            data["terminalGroupIds"] = terminal_group_ids

        if delivery_date_from is not None:
            if not isinstance(delivery_date_from, str):
                raise TypeError("type delivery_date_from != str")
            data["deliveryDateFrom"] = delivery_date_from

        if delivery_date_to is not None:
            if not isinstance(delivery_date_to, str):
                raise TypeError("type delivery_date_to != str")
            data["deliveryDateTo"] = delivery_date_to

        if statuses is not None:
            if not isinstance(statuses, list):
                raise TypeError("type statuses != list")
            data["statuses"] = statuses

        if has_problem is not None:
            if not isinstance(has_problem, bool):
                raise TypeError("type has_problem != list")
            data["hasProblem"] = has_problem

        if order_service_type is not None:
            if not isinstance(order_service_type, str):
                raise TypeError("type order_service_type != str")
            data["orderServiceType"] = order_service_type

        if search_text is not None:
            if not isinstance(search_text, str):
                raise TypeError("type search_text != str")
            data["searchText"] = search_text

        if time_to_cooking_error_timeout is not None:
            if not isinstance(time_to_cooking_error_timeout, int):
                raise TypeError("type time_to_cooking_error_timeout != int")
            data["timeToCookingErrorTimeout"] = time_to_cooking_error_timeout

        if cooking_timeout is not None:
            if not isinstance(cooking_timeout, int):
                raise TypeError("type cooking_timeout != int")
            data["cookingTimeout"] = cooking_timeout

        if sort_property is not None:
            if not isinstance(sort_property, str):
                raise TypeError("type sort_property != str")
            data["sortProperty"] = sort_property

        if sort_direction is not None:
            if not isinstance(sort_direction, str):
                raise TypeError("type sort_direction != str")
            data["sortDirection"] = sort_direction

        if rows_count is not None:
            if not isinstance(rows_count, int):
                raise TypeError("type rows_count != int")
            data["rowsCount"] = rows_count

        if source_keys is not None:
            if not isinstance(source_keys, list):
                raise TypeError("type source_keys != list")
            data["sourceKeys"] = source_keys

        if order_ids is not None:
            if not isinstance(order_ids, list):
                raise TypeError("type order_ids != list")
            data["orderIds"] = order_ids

        try:
            return self._post_request(
                url="/api/1/deliveries/by_delivery_date_and_source_key_and_filter",
                data=data,
                model_response_data=ByDeliveryDateAndSourceKeyAndFilter,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.by_delivery_date_and_status.__name__,
                                 f"Не удалось получить заказы: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.by_delivery_date_and_status.__name__,
                                 f"Не удалось: \n{err}")


class Notifications(BaseAPI):
    def send(self, order_source: str, order_id: str, additional_info: str, organization_id: str,
             message_type: str = "delivery_attention", timeout=BaseAPI.DEFAULT_TIMEOUT):
        """

        :param order_source:
        :param order_id:
        :param additional_info:
        :param organization_id:
        :param message_type:
        :return:
        """
        data = {
            "orderSource": order_source,
            "orderId": order_id,
            "additionalInfo": additional_info,
            "messageType": message_type,
            "organizationId": organization_id,

        }

        try:

            return self._post_request(
                url="/api/1/notifications/send",
                data=data,
                model_response_data=BaseResponseModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.send.__name__,
                                f"Не удалось отправить оповещение: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.send.__name__,
                                f"Не удалось: \n{err}")


class Employees(BaseAPI):

    def couriers(self, organization_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT):

        #     https://api-ru.iiko.services/api/1/employees/couriers
        data = {
            "organizationId": organization_id,
        }

        try:

            return self._post_request(
                url="/api/1/employees/couriers",
                data=data,
                model_response_data=CouriersModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.couriers.__name__,
                                f"Не удалось получить курьеров: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.couriers.__name__,
                                f"Не удалось: \n{err}")

    @experimental
    def employees_couriers_locations_by_time_offset(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    @experimental
    def employees_couriers_by_role(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    @experimental
    def employees_couriers_active_location_by_terminal(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    @experimental
    def employees_couriers_active_location(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    def employees_info(self, organization_id: str, id: str, timeout=BaseAPI.DEFAULT_TIMEOUT):
        data = {
            "organizationId": organization_id,
            "id": id
        }

        try:

            return self._post_request(
                url="/api/1/employees/info",
                data=data,
                model_response_data=BaseEInfoModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.couriers.__name__,
                                f"Не удалось получить информацию о сотруднике: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.couriers.__name__,
                                f"Не удалось: \n{err}")


class Customers(BaseAPI):
    def customer_info(self, organization_id: str, identifier: str, type: str, timeout=BaseAPI.DEFAULT_TIMEOUT)-> Union[CustomerInfoModel, CustomErrorModel]:
        """

        :param organization_id:
        :param identifier: Depending on type
        :param type: phone or  cardTrack or cardNumber or email or id
        :return:
        """
        data = {
            "organizationId": organization_id,
            "type": type,
        }
        if type == TypeRCI.phone.value:
            data[TypeRCI.phone.value] = identifier
        elif type == TypeRCI.card_track.value:
            data[TypeRCI.card_track.value] = identifier
        elif type == TypeRCI.card_number.value:
            data[TypeRCI.card_number.value] = identifier
        elif type == TypeRCI.email.value:
            data[TypeRCI.email.value] = identifier
        elif type == TypeRCI.id.value:
            data[TypeRCI.id.value] = identifier

        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/info",
                data=data,
                model_response_data=CustomerInfoModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_info.__name__,
                                f"Не удалось получить информацию о клиенте: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_info.__name__,
                                f"Не удалось: \n{err}")

    def customer_create_or_update(
        self,
        organization_id: str,
        phone: Optional[str] = None,
        card_track: Optional[str] = None,
        card_number: Optional[str] = None,
        name: Optional[str] = None,
        middle_name: Optional[str] = None,
        sur_name: Optional[str] = None,
        birthday: Optional[str] = None,
        email: Optional[str] = None,
        sex: Optional[str] = None,
        consent_status: Optional[str] = None,
        should_receive_promo_actions_info: Optional[bool] = None,
        referrer_id: Optional[str] = None,
        user_data: Optional[str] = None,
        id: str = None,
        timeout=BaseAPI.DEFAULT_TIMEOUT):

        data = {
            "organizationId": organization_id,
        }
        if id is not None:
            data['id'] = id
        if phone is not None:
            data['phone'] = phone
        if card_track is not None:
            data['cardTrack'] = card_track
        if card_number is not None:
            data['cardNumber'] = card_number
        if name is not None:
            data['name'] = name
        if middle_name is not None:
            data['middleName'] = middle_name
        if sur_name is not None:
            data['surName'] = sur_name
        if birthday is not None:
            data['birthday'] = birthday
        if email is not None:
            data['email'] = email
        if sex is not None:
            data['sex'] = sex
        if consent_status is not None:
            data['consentStatus'] = consent_status
        if should_receive_promo_actions_info is not None:
            data['shouldReceivePromoActionsInfo'] = should_receive_promo_actions_info
        if referrer_id is not None:
            data['referrerId'] = referrer_id
        if user_data is not None:
            data['userData'] = user_data

        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/create_or_update",
                data=data,
                model_response_data=CustomerCreateOrUpdateModel,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_create_or_update.__name__,
                                f"Не удалось создать или обновить клиента: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_create_or_update.__name__,
                                f"Не удалось: \n{err}")
    def customer_program_add(
        self,
        customer_id: str,
        program_id: str,
        organization_id: str,
        timeout=BaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "customerId": customer_id,
            "programId": program_id,
            "organizationId": organization_id,
        }
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/program/add",
                data=data,
                model_response_data=CustomerProgramAddResponse,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_program_add.__name__,
                                f"Не удалось подключить клиента к программе: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_program_add.__name__,
                                f"Не удалось: \n{err}")

    def customer_card_add(
        self,
        customer_id: str,
        card_track: str,
        card_number,
        organization_id: str,
        timeout=BaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "customerId": customer_id,
            "cardTrack": card_track,
            "cardNumber": card_number,
            "organizationId": organization_id,
        }
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/card/add",
                data=data,
                model_response_data=None,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_card_add.__name__,
                                f"Не удалось подключить карту клиенту: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_card_add.__name__,
                                f"Не удалось: \n{err}")
    def customer_card_delete(
        self,
        customer_id: str,
        card_track: str,
        organization_id: str,
        timeout=BaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "customerId": customer_id,
            "cardTrack": card_track,
            "organizationId": organization_id,
        }
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/card/remove",
                data=data,
                model_response_data=None,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_card_delete.__name__,
                                f"Не удалось подключить карту клиенту: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_card_delete.__name__,
                                f"Не удалось: \n{err}")
    def customer_wallet_hold(
        self,
        customer_id: str,
        wallet_id: str,
        sum: Union[int, float],
        organization_id: str,
        transaction_id: Optional[str] = None,
        comment: Optional[str]= None,
        timeout=BaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "customerId": customer_id,
            "walletId": wallet_id,
            "sum":sum,
            "organizationId": organization_id,
        }
        if transaction_id is not None:
            data["transactionId"] = transaction_id
        if comment is not None:
            data["comment"] = comment

        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/hold",
                data=data,
                model_response_data=WalletHoldResponse,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_hold.__name__,
                                f"Не удалось подключить карту клиенту: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_hold.__name__,
                                f"Не удалось: \n{err}")
    def customer_wallet_cancel_hold(
        self,
        organization_id: str,
        transaction_id: str,
        timeout=BaseAPI.DEFAULT_TIMEOUT
    ):

        data = {
            "organizationId": organization_id,
            "transactionId": transaction_id,
        }

        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/cancel_hold",
                data=data,
                model_response_data=None,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_cancel_hold.__name__,
                                f"Не удалось подключить карту клиенту: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_cancel_hold.__name__,
                                f"Не удалось: \n{err}")
    def customer_wallet_topup(
        self,
        customer_id: str,
        wallet_id: str,
        sum: Union[int, float],
        organization_id: str,
        comment: Optional[str]=None,
        timeout=BaseAPI.DEFAULT_TIMEOUT
    ):
        """
        Refill balance.
        Refill customer balance.
        :param customer_id: Customer id.
        :param wallet_id: Wallet id.
        :param sum: Sum of balance change. Must be possible.
        :param organization_id: Organization id.
        :param comment: Comment. Can be null.
        :param timeout:
        :return: dict response
        """

        data = {
            "customerId":customer_id,
            "walletId": wallet_id,
            "sum": sum,
            "organizationId": organization_id,
        }
        if comment is not None:
            data["comment"] = comment
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/topup",
                data=data,
                model_response_data=None,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_topup.__name__,
                                f"Не удалось подключить карту клиенту: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_topup.__name__,
                                f"Не удалось: \n{err}")

    def customer_wallet_chargeoff(
        self,
        customer_id: str,
        wallet_id: str,
        sum: Union[int, float],
        organization_id: str,
        comment: Optional[str]=None,
        timeout=BaseAPI.DEFAULT_TIMEOUT
    ):
        """
        Withdraw balance.
        Withdraw customer balance.
        :param customer_id: Customer id.
        :param wallet_id: Wallet id.
        :param sum: Sum of balance change. Must be possible.
        :param organization_id: Organization id.
        :param comment: Comment. Can be null.
        :param timeout:
        :return: dict response
        """

        data = {
            "customerId":customer_id,
            "walletId": wallet_id,
            "sum": sum,
            "organizationId": organization_id,
        }
        if comment is not None:
            data["comment"] = comment
        try:
            return self._post_request(
                url="/api/1/loyalty/iiko/customer/wallet/chargeoff",
                data=data,
                model_response_data=None,
                timeout=timeout
            )

        except requests.exceptions.RequestException as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_chargeoff.__name__,
                                f"Не удалось подключить карту клиенту: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_wallet_chargeoff.__name__,
                                f"Не удалось: \n{err}")





class IikoTransport(Orders, Deliveries, Employees, Address, DeliveryRestrictions, TerminalGroup, Menu, Dictionaries,
                    DiscountPromotion, Commands, Notifications, Customers,WebHook):
    pass
