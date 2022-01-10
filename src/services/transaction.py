# -*- coding: utf-8 -*-


# File: report.py	
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from src.models.report import Report
from src.models.transaction import TransactionModel, ErrorTransactionModel, CardTransactionModel, PreAuthTransactionModel
from src.enums.transaction import TransactionStatusEnum, TransactionTopicKeyEnum
from src.utils.logger import LoggerTask, Logger
from paydi_lib.exceptions import MissingData
from src.utils.datetime import get_current_time, convert_datetime_from_string, \
    date_range, \
    days_between
from datetime import datetime
from src.helpers.transaction import TransactionHelper
class TransactionService(object):
    @staticmethod
    def get_list_transactions(limit: int,
                              offset: int,
                              search_type: str,
                              search_status: str,
                              search_merchant: str,
                              search_bank_code: str,
                              ) -> list:
        filter = {}
        if search_status:
            filter['status'] = search_status
        if search_type:
            filter['obj_type'] = search_type
        if search_merchant:
            filter['odoo_contact_id'] = {
                "$regex": search_merchant    
            }
        if search_bank_code:
            filter['extract.bank_code'] = {
                "$regex": search_bank_code
            }
            
        Logger.debug(f'Filter = {filter}')
        
        transactions = TransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            },
            with_cache=False
        )
        
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2
    

    @staticmethod
    def get_list_error_transactions(limit: int,
                                    offset: int,
                                    search_app_ver: str,
                                    search_code: str,
                                    search_description: str,
                                    search_bank_code: str,
                                    search_merchant: str
                                    ) -> list:
        filter = {}
        if search_app_ver:
            filter['app_ver'] = {
                '$regex': search_app_ver
            }
        if search_code:
            filter['code'] = {
                '$regex': search_code
            }
        if search_description:
            filter['desc'] = {
                '$regex': search_description
            }
        if search_bank_code:
            filter['bank_code'] = {
                '$regex': search_bank_code
            }
        if search_merchant:
            filter['odoo_contact_id'] = {
                "$regex": search_merchant    
            }
            
        Logger.debug(f'Filter = {filter}')
        transactions = ErrorTransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            },
            with_cache=False
        )
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2

    @staticmethod
    def get_list_card_transactions(limit: int,
                                   offset: int,
                                   search_batch_no: str,
                                   search_app_ver: str,
                                   search_code: str,
                                   search_description: str,
                                   search_tranx_type: str,
                                   search_bank_code: str,
                                   search_merchant: str
                                   ) -> list:
        filter = {}
        if search_batch_no:
            filter['batch_no'] = {
                "$regex": search_batch_no
            }
        if search_app_ver:
            filter['app_ver'] = {
                "$regex": search_app_ver
            }
        if search_code:
            filter['code'] = {
                "$regex": search_code
            }
        if search_description:
            filter['desc'] = {
                "$regex": search_description
            }
        if search_tranx_type:
            filter['tranx_type'] = {
                "$regex": search_tranx_type
            }
        if search_bank_code:
            filter['bank_code'] = {
                '$regex': search_bank_code
            }
        if search_merchant:
            filter['odoo_contact_id'] = {
                "$regex": search_merchant    
            }
        
        Logger.debug(f'Filter = {filter}')
        transactions = CardTransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            },
            with_cache=False
        )
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2

    @staticmethod
    def get_list_pre_auth_transactions(limit: int,
                                       offset: int,
                                       search_invoice_no: str,
                                       search_bank_code: str,
                                       search_merchant: str
                                       ) -> list:
        filter = {}
        if search_invoice_no:
            filter['invoice_no'] = {
                "$regex": search_invoice_no
            }
        if search_bank_code:
            filter['bank_code'] = {
                '$regex': search_bank_code
            }
        if search_merchant:
            filter['odoo_contact_id'] = {
                "$regex": search_merchant    
            }
        
        transactions = PreAuthTransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            },
            with_cache=False
        )
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2

    @staticmethod
    def get_transactions_statistic(query: dict):
        """Example:
            query: {
                'from_date': '05/01/2022',
                'to_date': '05/02/2022'
            }
            
        """
        filter = {}
        
        to_date = datetime.utcnow()
        # from_date = datetime.utcnow() - 3600 * 24
        
        if query and query.get('from_date'):

            from_date = convert_datetime_from_string(query.get('from_date'), '%d/%m/%Y')
            _days_number = days_between(from_date, to_date)

            if _days_number > 50:
                raise MissingData(message='Chỉ xem tối đa từ 50 ngày trước')

            if query.get('to_date'):
                to_date = convert_datetime_from_string(query.get('to_date'), '%d/%m/%Y') or datetime.utcnow()
        filter['created_time'] = {
            "$gt": from_date,
            "$lt": to_date,
        }
        types = {
            '1': 'VISA/JCB',
            '2': 'NAPAS',
            '3': 'MasterCard'
        }
        if query and query.get('search_merchant'):
            filter['odoo_contact_id'] = query.get('search_merchant')
        
        _statistics_qr_code = {
            'total_transactions': TransactionModel.count_with_filter(
                filter=TransactionHelper.get_filter_by_obj_type(filter, 'qr_code')
            ),
            'total_amount': TransactionModel.sum_with_filter(
                filter=TransactionHelper.get_filter_by_obj_type(filter, 'qr_code'),
                sum_field_name='total_amount'
            )    
        }
        Logger.debug(f'Statistic QR code = {_statistics_qr_code}')
        _statistics_card = {
            'total_transactions': TransactionModel.count_with_filter(
                filter=TransactionHelper.get_filter_by_obj_type(filter, 'card')
            ),
            'total_amount': TransactionModel.sum_with_filter(
                filter=TransactionHelper.get_filter_by_obj_type(filter, 'card'),
                sum_field_name='total_amount'
            )
        }
        Logger.debug(f'Statistic card = {_statistics_card}')
        _statistics_card_types = [
            {
                'name': val,
                'total_transactions': TransactionModel.count_with_filter(
                    filter=TransactionHelper.get_filter_card_type(filter, _code)
                ),
                'total_amount': TransactionModel.sum_with_filter(
                    filter=TransactionHelper.get_filter_card_type(filter, _code),
                    sum_field_name='total_amount'
                )
            }
            for _code, val in types.items()
        ]
        Logger.debug(f'Statistic card types = {_statistics_card_types}')
        return {
            'card': {
                'total_amount': _statistics_card.get('total_amount'),
                'total_transactions': _statistics_card.get('total_transactions'),
                'types': _statistics_card_types
            },
            'qr_code': _statistics_qr_code,
            'total_amount': sum(
                map(lambda x: x.get('total_amount'), [_statistics_card, _statistics_qr_code])
            ),
            'total_transactions': sum(
                map(lambda x: x.get('total_transactions'), [_statistics_card, _statistics_qr_code])
            )
        }